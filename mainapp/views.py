from django.shortcuts import render, get_object_or_404
from mainapp.models import Product, ProductCategory
import random
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def get_basket(request):
    return request.user.is_authenticated and request.user.basket.all() or []


def get_menu():
    return ProductCategory.objects.filter(is_active=True)


def index(request):
    context = {
        'page_title': 'главная',
        'basket': get_basket(request),
    }
    return render(request, 'mainapp/index.html', context)


def products(request):
    hot_product_pk = random.choice(Product.objects.filter(is_active=True).values_list('pk', flat=True))
    hot_product = Product.objects.get(pk=hot_product_pk)

    same_products = hot_product.category.product_set.filter(is_active=True).exclude(pk=hot_product.pk)

    context = {
        'page_title': 'каталог',
        'categories': get_menu(),
        'basket': get_basket(request),
        'hot_product': hot_product,
        'same_products': same_products,
    }
    return render(request, 'mainapp/products.html', context)


def category_products(request, pk, page=1):
    if pk == '0':
        category = {'pk': 0, 'name': 'все'}
        products = Product.objects.filter(is_active=True)
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        products = category.product_set.filter(is_active=True)

    products_paginator = Paginator(products, 3)
    try:
        products = products_paginator.page(page)
    except PageNotAnInteger:
        products = products_paginator.page(1)
    except EmptyPage:
        products = products_paginator.page(products_paginator.num_pages)


    context = {
        'page_title': 'каталог',
        'categories': get_menu(),
        'products': products,
        'category': category,
        'basket': get_basket(request),
    }
    return render(request, 'mainapp/category_products.html', context)


def product_page(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'page_title': 'каталог',
        'categories': get_menu(),
        'category': product.category,
        'basket': get_basket(request),
        'product': product,
    }
    return render(request, 'mainapp/product.html', context)


def contact(request):
    locations = [
        {
            'city': 'Москва',
            'phone': '+7-495-888-8888',
            'email': 'info@geekshop.ru',
            'address': 'В пределах МКАД',
        },
        {
            'city': 'Санкт-Петербург',
            'phone': '+7-812-888-8888',
            'email': 'info@geekshop.ru',
            'address': 'В пределах КАД',
        },
        {
            'city': 'Владивосток',
            'phone': '+7-111-888-8888',
            'email': 'info@geekshop.ru',
            'address': 'В пределах города',
        },
    ]
    context = {
        'page_title': 'контакты',
        'locations': locations,
        'basket': get_basket(request),
    }
    return render(request, 'mainapp/contact.html', context)
