# myapp/models.py

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=200, null=True, blank=True)
    tags = models.CharField(max_length=200, null=True, blank=True)

    created_at = models.DateTimeField("Created at", auto_now_add=True)

    def __str__(self):
        return self.name


class ProductInventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    inventory_count = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField("Created at", auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - Inventory: {self.inventory_count}"