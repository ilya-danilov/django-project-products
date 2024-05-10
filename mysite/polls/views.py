from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404

from .models import Category, Product, Promotion, Review


def main(request):
    latest_product_list = Product.objects.order_by('-created')[:5]
    context = {'latest_product_list': latest_product_list}
    return render(request, 'polls/index.html', context)

# def main(request):
#     return render(
#         request,
#         'polls/index.html',
#         context={
#             'categories': Category.objects.count(),
#             'products': Product.objects.count(),
#             'promotions': Promotion.objects.count(),
#             'reviews': Review.objects.count(),
#         }
#     )

def detail(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, 'polls/detail.html', {'product': product})