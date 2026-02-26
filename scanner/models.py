from django.db import models

class Product(models.Model):
    barcode = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    qty = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.barcode})"
    
    
class Scanhistory(models.Model):
    barcode = models.CharField(max_length=50)
    name = models.CharField(max_length=255, null=True, blank=True)
    scanned_qty = models.IntegerField()
    scanned_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Scanned {self.name} ({self.barcode}) at {self.scanned_at}"
    
    
