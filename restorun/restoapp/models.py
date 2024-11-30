from django.db import models

class Item(models.Model):
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    expiry_date = models.DateField()
    purchase_date = models.DateField()
    supplier = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name
