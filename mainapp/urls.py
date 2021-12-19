from django.urls import path, re_path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name='index'),
    path('catalog/', mainapp.products, name='products'),
    path('contacts/', mainapp.contact, name='contact'),
    re_path(r'^category/(?P<pk>\d+)/products/$', mainapp.category_products, name='category_products'),
    re_path(r'^category/(?P<pk>\d+)/products/(?P<page>\d+)/$', mainapp.category_products, name='category_products_pagination'),
    re_path(r'^product/(?P<pk>\d+)/$', mainapp.product_page, name='product_page'),
]
