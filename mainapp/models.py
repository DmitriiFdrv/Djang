from django.db import models

# SomeModel.objects.filter(id=id).delete() - для себя, удаление элемента модели
class ProductCategory(models.Model):
    name = models.CharField('имя категории', max_length=64)
    description = models.TextField('описание категории', blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, verbose_name='категория продукта', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='имя продукта', max_length=128)
    image = models.ImageField(upload_to='products_images', blank=True)
    short_desc = models.CharField(verbose_name='краткое описание продукта', max_length=64, blank=True)
    description = models.TextField(verbose_name='описание продукта', blank=True)
    price = models.DecimalField(verbose_name='цена продукта', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField('количество на складе', default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"
