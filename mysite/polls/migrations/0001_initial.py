# Generated by Django 5.0.3 on 2024-05-06 22:02

import datetime
import django.core.validators
import django.db.models.deletion
import polls.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, default=polls.models.get_datetime, null=True, validators=[polls.models.check_created], verbose_name='created')),
                ('modified', models.DateTimeField(blank=True, default=polls.models.get_datetime, null=True, validators=[polls.models.check_modified], verbose_name='modified')),
                ('title', models.TextField(validators=[django.core.validators.MaxLengthValidator(100)], verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(1000)], verbose_name='description')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'db_table': '"api_data"."categories"',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, default=polls.models.get_datetime, null=True, validators=[polls.models.check_created], verbose_name='created')),
                ('modified', models.DateTimeField(blank=True, default=polls.models.get_datetime, null=True, validators=[polls.models.check_modified], verbose_name='modified')),
                ('title', models.TextField(validators=[django.core.validators.MaxLengthValidator(200)], verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(2000)], verbose_name='description')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=7, validators=[django.core.validators.MinValueValidator(0)], verbose_name='price')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.category', verbose_name='category')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'db_table': '"api_data"."products"',
                'ordering': ['category', 'title', 'price'],
            },
        ),
        migrations.CreateModel(
            name='ProductToPromotion',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, default=polls.models.get_datetime, null=True, validators=[polls.models.check_created], verbose_name='created')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'Relationship product to promotion',
                'verbose_name_plural': 'Relationships product to promotion',
                'db_table': '"api_data"."product_to_promotion"',
            },
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, default=polls.models.get_datetime, null=True, validators=[polls.models.check_created], verbose_name='created')),
                ('modified', models.DateTimeField(blank=True, default=polls.models.get_datetime, null=True, validators=[polls.models.check_modified], verbose_name='modified')),
                ('title', models.TextField(validators=[django.core.validators.MaxLengthValidator(200)], verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(2000)], verbose_name='description')),
                ('discount_amount', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)], verbose_name='discount amount')),
                ('start_date', models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(2024, 5, 6))], verbose_name='start date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='end date')),
                ('products', models.ManyToManyField(through='polls.ProductToPromotion', to='polls.product', verbose_name='products')),
            ],
            options={
                'verbose_name': 'promotion',
                'verbose_name_plural': 'promotions',
                'db_table': '"api_data"."promotions"',
                'ordering': ['discount_amount'],
            },
        ),
        migrations.AddField(
            model_name='producttopromotion',
            name='promotion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.promotion', verbose_name='promotion'),
        ),
        migrations.AddField(
            model_name='product',
            name='promotions',
            field=models.ManyToManyField(through='polls.ProductToPromotion', to='polls.promotion', verbose_name='promotions'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, default=polls.models.get_datetime, null=True, validators=[polls.models.check_created], verbose_name='created')),
                ('modified', models.DateTimeField(blank=True, default=polls.models.get_datetime, null=True, validators=[polls.models.check_modified], verbose_name='modified')),
                ('text', models.TextField(validators=[django.core.validators.MaxLengthValidator(1000)], verbose_name='text')),
                ('rating', models.PositiveSmallIntegerField(blank=True, default=5, null=True, validators=[django.core.validators.MaxValueValidator(5)], verbose_name='rating')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.product', verbose_name='product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'review',
                'verbose_name_plural': 'reviews',
                'db_table': '"api_data"."reviews"',
                'ordering': ['rating'],
            },
        ),
        migrations.CreateModel(
            name='CategoryToCategory',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, default=polls.models.get_datetime, null=True, validators=[polls.models.check_created], verbose_name='created')),
                ('child_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_categories', to='polls.category', verbose_name='child_category')),
                ('parent_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_categories', to='polls.category', verbose_name='parent_category')),
            ],
            options={
                'verbose_name': 'Relationship category to category',
                'verbose_name_plural': 'Relationships category to category',
                'db_table': '"api_data"."category_to_category"',
                'unique_together': {('parent_category', 'child_category')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='producttopromotion',
            unique_together={('product', 'promotion')},
        ),
    ]
