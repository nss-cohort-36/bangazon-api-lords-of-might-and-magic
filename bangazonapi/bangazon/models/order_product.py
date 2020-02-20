from django.db import models
from .order import Order
from .customer import Customer


class OrderProduct(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        ordering = ("order",)
