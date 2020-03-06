from django.db import models
from .customer import Customer
from .product_type import ProductType
from .order_product import OrderProduct
from safedelete.models import SafeDeleteModel
from safedelete.models import HARD_DELETE_NOCASCADE


class Product(SafeDeleteModel):

    _safedelete_policy = HARD_DELETE_NOCASCADE

    created_at = models.DateField(auto_now=False, auto_now_add=True)
    name = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    location = models.CharField(max_length=75)
    image_path = models.CharField(max_length=255)
    product_type = models.ForeignKey(ProductType, on_delete=models.DO_NOTHING)
    inventory = models.IntegerField(default=0)

    class Meta:
        ordering = ("created_at",)
        verbose_name = ("product")
        verbose_name_plural = ("products")

    def __str__(self):
        return self.name
