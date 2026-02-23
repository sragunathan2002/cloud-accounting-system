from django.contrib import admin
from .models import Ledger, Supplier, Purchase, Customer, Sale, Item, HSN

@admin.register(Ledger)
class LedgerAdmin(admin.ModelAdmin):
    list_display = ('name', 'ledger_type', 'opening_balance')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'gstin', 'state')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'gstin', 'state')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'item',
        'quantity',
        'rate',
        'gst_percent',
        'subtotal',
        'gst_amount',
        'total'
    )

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = (
    'item',
    'quantity',
    'rate',
    'gst_percent',
    'subtotal',
    'gst_amount',
    'total'
)
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_hsn_code', 'unit', 'stock_quantity')

    def get_hsn_code(self, obj):
        return obj.hsn.code
    get_hsn_code.short_description = 'HSN Code'


@admin.register(HSN)
class HSNAdmin(admin.ModelAdmin):
    list_display = ('code', 'gst_rate')