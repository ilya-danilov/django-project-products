from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator
from django.utils import timezone
from uuid import uuid4
from datetime import datetime


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, blank=True, editable=False, default=uuid4)

    class Meta:
        abstract = True


# class CreatedMixin(models.Model):
#     created = models.DateTimeField(null=True, blank=True, default=datetime.now)

#     class Meta:
#         abstract = True


# class ModifiedMixin(models.Model):
#     modified = models.DateTimeField(null=True, blank=True, default=datetime.now)

#     class Meta:
#         abstract = True


class Product(UUIDMixin):
    title = models.TextField(null=False, blank=False, validators=[MaxLengthValidator(100)])
    price = models.DecimalField(null=False, blank=False, max_digits=7, decimal_places=2, validators=[MinValueValidator(0.01)])
    category = models.TextField(null=False, blank=False, validators=[MaxLengthValidator(50)])

    promotions = models.ManyToManyField('Promotion', through='ProductToPromotion')

    def __str__(self) -> str:
        return f'{self.title} ({self.category}), {self.price} rubles'

    class Meta:
        db_table = '"app_data"."products"'

class Promotion(UUIDMixin):
    title = models.TextField(null=False, blank=False, validators=[MaxLengthValidator(400)])
    discount_amount = models.PositiveSmallIntegerField(null=False, blank=False, validators=[MaxValueValidator(100)])
    start_date = models.DateField(null=False, blank=False, validators=[MinValueValidator(timezone.now().date())])
    end_date = models.DateField(null=True, blank=True)

    def clean(self):
        super().clean()
        if self.end_date and self.start_date > self.end_date:
            raise ValidationError({
                'end_date': 'The value in the <end_date> field should be greater than or equal to the value in the <start_date> field.',
            })
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        db_table = '"app_data"."promotions"'


class Review(UUIDMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.TextField(null=False, blank=False, validators=[MaxLengthValidator(400)])
    rating = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MaxValueValidator(10)])

    def __str__(self) -> str:
        return f'{self.product}: {self.content}, rating {self.rating}/5'
    
    class Meta:
        db_table = '"app_data"."reviews"'

class ProductToPromotion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.product}: {self.promotion}'

    class Meta:
        db_table = '"app_data"."product_to_promotion"'
        unique_together = (
            ('product', 'promotion'),
        )
