from django.db import models
from django.conf import settings


class Category(models.Model):
    category_name = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.category_name


class Debtor(models.Model):
    in_debt = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='users_in_debt',
                                on_delete=models.CASCADE)
    owes = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='users_owes',
                             on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, related_name='category')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
