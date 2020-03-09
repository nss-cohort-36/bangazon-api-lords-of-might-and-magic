from django.db import models
from django.db.models import F
from django.contrib.auth.models import User


class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField()
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=12, null = True)



    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    # class Meta:
    #     ordering = (F('user.date_joined').asc(nulls_last=True),)
