from django.db import models
from mainapp.models import Product
from authapp.models import ShopUser

class Basket(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE, related_name='basket')
    quantity = models.PositiveIntegerField('количество', default=0)
    add_datetime = models.DateTimeField('время', auto_now_add=True)


    @property
    def product_cost(self):
        "return cost of all products this type"
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        "return total quantity for user"
        # _items = Basket.objects.filter(user=self.user)
        # _items = self.user.basket_set.all()
        return sum(map(lambda x: x.quantity, self.user.basket.all()))
        # return sum(self.user.basket.values_list('quantity', flat=True))

    @property
    def total_cost(self):
        "return total cost for user"
        # _items = Basket.objects.filter(user=self.user)
        # _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
        return sum(map(lambda x: x.product_cost, self.user.basket.all()))
