# transactions/urls.py
from django.urls import path
from .views import TransactionListCreateView, get_average_buy_price_and_balance

urlpatterns = [
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('average_buy_price_balance/', get_average_buy_price_and_balance, name='average-buy-price-balance'),
]
