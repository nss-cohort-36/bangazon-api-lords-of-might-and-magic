from django.db import models
from .customer import Customer
from .product import Product
from .payment_type import PaymentType
from .order_product import OrderProduct


class Order(models.Model):

    created_at = models.DateField(auto_now=False, auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.DO_NOTHING, null=True, default=None)
    products = models.ManyToManyField(Product, through=OrderProduct)

    class Meta:
        ordering = ("created_at",)
        verbose_name = ("order",)
        verbose_name_plural = ("orders",)

    def __str__(self):
        return f'Paid with {self.payment_type} for {self.customer}'
