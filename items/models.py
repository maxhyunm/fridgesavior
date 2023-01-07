from django.db import models
from users.models import User


class ProductCategory(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    expire_within = models.PositiveSmallIntegerField(default=0)
    detail = models.TextField(null=True, blank=True, default='')

    def __str__(self):
        return self.name


class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateField()
    amount = models.PositiveSmallIntegerField(default=0)
    unit = models.CharField(max_length=10)
    detail = models.TextField(null=True, blank=True, default='')

    def __str__(self):
        return f'{self.product.name}_{self.amount}{self.unit}_{self.expired_at}까지'






