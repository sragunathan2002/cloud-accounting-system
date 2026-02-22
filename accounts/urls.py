from django.urls import path
from . import views

urlpatterns = [
    path('monthly-performance/', views.monthly_performance, name='monthly_performance'),
    path('profit-loss/', views.profit_loss, name='profit_loss'),
    path('balance-sheet/', views.balance_sheet, name='balance_sheet'),
    path('gstr1/', views.gstr1_report, name='gstr1'),
    path('gstr3b/', views.gstr3b_report, name='gstr3b'),
]

