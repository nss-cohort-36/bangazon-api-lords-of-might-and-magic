from django.db import models
from .customer import Customer


class PaymentType(models.Model):

    merchant_name = models.CharField(max_length=25)
    acct_number = models.CharField(max_length=25)
    expiration_date = models.DateField(auto_now=False, auto_now_add=False)
    created_at = models.DateField(auto_now=False, auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        ordering = ("created_at",)
        verbose_name = ("payment_type",)
        verbose_name_plural = ("payment_types",)

    def __str__(self):
        return f'{self.merchant_name} {self.acct_number}'
