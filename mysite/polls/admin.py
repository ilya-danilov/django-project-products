from django.contrib import admin
from .models import Product, Promotion, Review, Category, CategoryToCategory, ProductToPromotion
from .forms import ProductForm, PromotionForm, ReviewForm

# inlines

class CategoryToCategoryInline(admin.TabularInline):
    model = CategoryToCategory
    extra = 1
    fk_name = 'parent_category'


class ProductToPromotionInline(admin.TabularInline):
    model = ProductToPromotion
    extra = 1

# admins

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    inlines = (CategoryToCategoryInline,)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    form = ProductForm
    inlines = (ProductToPromotionInline,)


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    model = Promotion
    form = PromotionForm
    inlines = (ProductToPromotionInline,)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    model = Review
    form = ReviewForm
    extra = 1