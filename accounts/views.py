from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .models import Sale, Purchase


from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .models import Sale, Purchase


def monthly_performance(request):
    sales_qs = (
        Sale.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total_sales=Sum('total_amount'))
        .order_by('month')
    )

    purchase_qs = (
        Purchase.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total_purchase=Sum('total_amount'))
        .order_by('month')
    )

    sales_data = []
    purchase_data = []

    for s in sales_qs:
        sales_data.append({
            'month': s['month'].strftime('%b %Y'),
            'total': float(s['total_sales'] or 0)
        })

    for p in purchase_qs:
        purchase_data.append({
            'month': p['month'].strftime('%b %Y'),
            'total': float(p['total_purchase'] or 0)
        })

    return render(request, 'accounts/monthly_performance.html', {
        'sales': sales_data,
        'purchases': purchase_data
    })

from django.db.models import Sum

def profit_loss(request):
    total_sales = Sale.objects.aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    total_purchases = Purchase.objects.aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    profit = total_sales - total_purchases

    return render(request, 'accounts/profit_loss.html', {
        'total_sales': total_sales,
        'total_purchases': total_purchases,
        'profit': profit
    })

def balance_sheet(request):
    from django.db.models import Sum
    from .models import Sale, Purchase

    total_sales = Sale.objects.aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    total_purchases = Purchase.objects.aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    assets = total_sales
    liabilities = total_purchases
    capital = assets - liabilities

    return render(request, 'accounts/balance_sheet.html', {
        'total_sales': total_sales,
        'total_purchases': total_purchases,
        'assets': assets,
        'liabilities': liabilities,
        'capital': capital
    })
from django.db.models import Sum
from .models import Sale, Purchase

def gstr1_report(request):
    sales = Sale.objects.all()

    total_taxable = sales.aggregate(
        total=Sum('taxable_value')
    )['total'] or 0

    total_cgst = sales.aggregate(
        total=Sum('cgst')
    )['total'] or 0

    total_sgst = sales.aggregate(
        total=Sum('sgst')
    )['total'] or 0

    total_igst = sales.aggregate(
        total=Sum('igst')
    )['total'] or 0

    return render(request, 'accounts/gstr1.html', {
        'sales': sales,
        'total_taxable': total_taxable,
        'total_cgst': total_cgst,
        'total_sgst': total_sgst,
        'total_igst': total_igst,
    })
def gstr3b_report(request):
    sales = Sale.objects.all()
    purchases = Purchase.objects.all()

    output_gst = (
        sales.aggregate(total=Sum('cgst'))['total'] or 0
    ) + (
        sales.aggregate(total=Sum('sgst'))['total'] or 0
    ) + (
        sales.aggregate(total=Sum('igst'))['total'] or 0
    )

    input_gst = (
        purchases.aggregate(total=Sum('cgst'))['total'] or 0
    ) + (
        purchases.aggregate(total=Sum('sgst'))['total'] or 0
    ) + (
        purchases.aggregate(total=Sum('igst'))['total'] or 0
    )

    net_gst = output_gst - input_gst

    return render(request, 'accounts/gstr3b.html', {
        'output_gst': output_gst,
        'input_gst': input_gst,
        'net_gst': net_gst,
    })