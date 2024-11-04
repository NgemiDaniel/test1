from django.shortcuts import render, redirect
from product.models import Product





def indexview(request):
    products = Product.objects.all()
    return render(request, 'base/index.html', {'products':products})

