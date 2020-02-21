from django.db import models
from django.db.models import F
from django.contrib.auth.models import User


class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = (F('user.date_joined').asc(nulls_last=True),)
