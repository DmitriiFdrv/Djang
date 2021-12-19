import os
import json

from django.core.management.base import BaseCommand

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from django.conf import settings


def load_from_json(file_name):
    with open(
            os.path.join(settings.JSON_PATH, f'{file_name}.json'),
            encoding='utf-8'
    ) as infile:
        return json.load(infile)


class Command(BaseCommand):
    help = 'Fill DB new data'

    def handle(self, *args, **options):
        categories = load_from_json('categories')

        ProductCategory.objects.all().delete()
        [ProductCategory.objects.create(**category) for category in categories]

        products = load_from_json('products')
        Product.objects.all().delete()  # all() -> QuerySet -> .first() -> concrete object
        for product in products:
            category_name = product['category']
            # Получаем категорию по имени
            _category = ProductCategory.objects.get(name=category_name)
            # Заменяем название категории объектом
            product['category'] = _category
            new_product = Product(**product)
            new_product.save()


        if not ShopUser.objects.filter(username='django').exists():
            ShopUser.objects.create_superuser(username='django', email='admin@geekshop.local', password='geekbrains')
