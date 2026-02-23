from typing import Self
from django.db import models

class Ledger(models.Model):
    LEDGER_TYPES = [
        ('ASSET', 'Asset'),
        ('LIABILITY', 'Liability'),
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]

    name = models.CharField(max_length=100)
    ledger_type = models.CharField(max_length=20, choices=LEDGER_TYPES)
    opening_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.name
    
class Supplier(models.Model):
    name = models.CharField(max_length=150)
    gstin = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True)
    state = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Customer(models.Model):
    name = models.CharField(max_length=150)
    gstin = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True)
    state = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class HSN(models.Model):
    code = models.CharField(max_length=20)
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.code} ({self.gst_rate}%)"


class Item(models.Model):
    name = models.CharField(max_length=150)
    hsn = models.ForeignKey(HSN, on_delete=models.PROTECT)
    unit = models.CharField(max_length=20, default='Nos')
    stock_quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class Purchase(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    gst_percent = models.DecimalField(max_digits=5, decimal_places=2, default=18)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.rate
        self.gst_amount = (self.subtotal * self.gst_percent) / 100
        self.total = self.subtotal + self.gst_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.item)

class Sale(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    gst_percent = models.DecimalField(max_digits=5, decimal_places=2)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.rate
        self.gst_amount = (self.subtotal * self.gst_percent) / 100
        self.total = self.subtotal + self.gst_amount
        super().save(*args, **kwargs)