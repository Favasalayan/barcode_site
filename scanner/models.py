from django.db import models

class Product(models.Model):
    barcode = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    qty = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.barcode})"
    
