from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator
from django.conf.global_settings import AUTH_USER_MODEL
from django.utils import timezone as django_timezone
from django.utils.translation import gettext_lazy as _
from uuid import uuid4
from datetime import datetime, timezone


def get_datetime():
    return datetime.now(timezone.utc)

def check_created(date: datetime) -> None:
    if date > get_datetime():
        raise ValidationError(
            _('Datetime is bigger than current datetime!'),
            params={'created': date}
        )

def check_modified(date: datetime) -> None:
    if date > get_datetime():
        raise ValidationError(
            _('Datetime is bigger than current datetime!'),
            params={'modified': date}
        )


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, blank=True, editable=False, default=uuid4)

    class Meta:
        abstract = True


class CreatedMixin(models.Model):
    created = models.DateTimeField(
        _('created'),
        null=True, blank=True,
        default=get_datetime, 
        validators=[
            check_created,
        ]
    )

    class Meta:
        abstract = True


class ModifiedMixin(models.Model):
    modified = models.DateTimeField(
        _('modified'),
        null=True, blank=True,
        default=get_datetime, 
        validators=[
            check_modified,
        ]
    )

    class Meta:
        abstract = True


class Category(UUIDMixin, CreatedMixin, ModifiedMixin):
    title = models.TextField(_('title'), null=False, blank=False, validators=[MaxLengthValidator(100)])
    description = models.TextField(_('description'), null=True, blank=True, validators=[MaxLengthValidator(1000)])
    # cover = models.ImageField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        db_table = '"api_data"."categories"'
        ordering = ['title']
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class CategoryToCategory(UUIDMixin, CreatedMixin):
    parent_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('parent_category'), related_name='child_categories')
    child_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('child_category'), related_name='parent_categories')

    def __str__(self) -> str:
        return f'{self.parent_category} - {self.child_category}'

    class Meta:
        db_table = '"api_data"."category_to_category"'
        unique_together = (
            ('parent_category', 'child_category'),
        )
        verbose_name = _('Relationship category to category')
        verbose_name_plural = _('Relationships category to category')


class Product(UUIDMixin, CreatedMixin, ModifiedMixin):
    title = models.TextField(_('title'), null=False, blank=False, validators=[MaxLengthValidator(200)])
    description = models.TextField(_('description'), null=True, blank=True, validators=[MaxLengthValidator(2000)])
    # specifications = models.JSONField(blank=True, null=True)
    price = models.DecimalField(_('price'), null=False, blank=False, max_digits=7, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    # cover = models.ImageField(null=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('category'))
    promotions = models.ManyToManyField('Promotion', through='ProductToPromotion', verbose_name=_('promotions'))

    def __str__(self) -> str:
        return f'{self.title} ({self.price} {_("rubles")})'

    class Meta:
        db_table = '"api_data"."products"'
        ordering = ['category', 'title', 'price']
        verbose_name = _('product')
        verbose_name_plural = _('products')


class Promotion(UUIDMixin, CreatedMixin, ModifiedMixin):
    title = models.TextField(_('title'), null=False, blank=False, validators=[MaxLengthValidator(200)])
    description = models.TextField(_('description'), null=True, blank=True, validators=[MaxLengthValidator(2000)])
    discount_amount = models.PositiveSmallIntegerField(_('discount amount'), null=False, blank=False, validators=[MaxValueValidator(100)], default=0)
    start_date = models.DateField(_('start date'), null=False, blank=False, validators=[MinValueValidator(django_timezone.now().date())])
    end_date = models.DateField(_('end date'), null=True, blank=True)

    products = models.ManyToManyField(Product, through='ProductToPromotion', verbose_name=_('products'))

    def clean(self):
        super().clean()
        if self.end_date and self.start_date > self.end_date:
            raise ValidationError({
                'end_date': _(f'The {self.end_date} should be greater than or equal to the {self.start_date}'),
            })
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        db_table = '"api_data"."promotions"'
        ordering = ['discount_amount']
        verbose_name = _('promotion')
        verbose_name_plural = _('promotions')


class Review(UUIDMixin, CreatedMixin, ModifiedMixin):
    text = models.TextField(_('text'), null=False, blank=False, validators=[MaxLengthValidator(1000)])
    rating = models.PositiveSmallIntegerField(_('rating'), null=True, blank=True, validators=[MaxValueValidator(5)], default=5)

    # user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'))

    def __str__(self) -> str:
        return f'{self.text}; {_("rating")} {self.rating}/5'
    
    class Meta:
        db_table = '"api_data"."reviews"'
        ordering = ['rating']
        verbose_name = _('review')
        verbose_name_plural = _('reviews')


class ProductToPromotion(UUIDMixin, CreatedMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'))
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, verbose_name=_('promotion'))

    def __str__(self) -> str:
        return f'{self.product} - {self.promotion}'

    class Meta:
        db_table = '"api_data"."product_to_promotion"'
        unique_together = (
            ('product', 'promotion'),
        )
        verbose_name = _('Relationship product to promotion')
        verbose_name_plural = _('Relationships product to promotion')
