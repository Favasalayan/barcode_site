from django.db import models


class Product(models.Model):
    barcode = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    required_qty = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.barcode})"


class Scanhistory(models.Model):
    barcode = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    required_qty = models.IntegerField()
    available_qty = models.IntegerField()
    scan_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.scan_time}"