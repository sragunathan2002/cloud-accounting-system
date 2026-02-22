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
    invoice_no = models.CharField(max_length=50)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    taxable_value = models.DecimalField(max_digits=12, decimal_places=2)
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2, editable=False)

    cgst = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    sgst = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    igst = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)

    total_amount = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    is_interstate = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        # 🔹 Auto GST from HSN
        self.gst_rate = self.item.hsn.gst_rate

        gst_amount = (self.taxable_value * self.gst_rate) / 100

        if self.is_interstate:
            self.igst = gst_amount
            self.cgst = 0
            self.sgst = 0
        else:
            self.cgst = gst_amount / 2
            self.sgst = gst_amount / 2
            self.igst = 0

        self.total_amount = self.taxable_value + gst_amount

        # 🔹 Stock increase (only on new purchase)
        if not self.pk:
            self.item.stock_quantity += self.quantity
            self.item.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_no

class Sale(models.Model):
    invoice_no = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    taxable_value = models.DecimalField(max_digits=12, decimal_places=2)
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2, editable=False)

    cgst = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    sgst = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    igst = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)

    total_amount = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    is_interstate = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        # 🔹 Auto GST from HSN
        self.gst_rate = self.item.hsn.gst_rate

        gst_amount = (self.taxable_value * self.gst_rate) / 100

        if self.is_interstate:
            self.igst = gst_amount
            self.cgst = 0
            self.sgst = 0
        else:
            self.cgst = gst_amount / 2
            self.sgst = gst_amount / 2
            self.igst = 0

        self.total_amount = self.taxable_value + gst_amount

        # 🔹 Stock decrease (only on new sale)
        if not self.pk:
            self.item.stock_quantity -= self.quantity
            self.item.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_no
