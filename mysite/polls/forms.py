from .models import Product, Promotion, Review
from django import forms


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'price': forms.NumberInput(attrs={'min': '0', 'step': '1.00', 'max': '99999.99'}),
        }


class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = '__all__'
        widgets = {
            'discount_amount': forms.NumberInput(attrs={'min': '0', 'step': '1', 'max': '100'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
        widgets = {
            'rating': forms.NumberInput(attrs={'min': '0', 'step': '1', 'max': '5'}),
        }