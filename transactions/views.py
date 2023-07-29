from rest_framework import generics
from .models import Transaction
from .serializers import TransactionSerializer
import datetime
from django.http import JsonResponse
from django.db.models import Sum, F

class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer



def get_average_buy_price_and_balance(request):
    if 'date' not in request.GET:
        return JsonResponse({'error': 'Please provide the date parameter.'}, status=400)
    
    date_str = request.GET['date']
    company = request.GET['company']

    try:
        trade_date = datetime.datetime.strptime(date_str, '%d/%m/%Y').date()

    except ValueError:
        return JsonResponse({'error': 'Invalid date format. Use DD/MM/YYYY format.'}, status=400)
    transactions_before_date = Transaction.objects.filter(trade_date__lte=trade_date).order_by('trade_date', 'id')
    balance_quantity = 0
    total_cost = 0
    buy_transactions = []

    for transaction in transactions_before_date:
        if transaction.trade_type == 'BUY':
            balance_quantity += transaction.quantity
            total_cost += transaction.quantity * transaction.price_per_share
            buy_transactions.append(transaction)
        elif transaction.trade_type == 'SELL':
            sell_quantity = transaction.quantity
            for buy_transaction in buy_transactions:
                if buy_transaction.quantity <= sell_quantity:
                    total_cost -= buy_transaction.quantity * buy_transaction.price
                    sell_quantity -= buy_transaction.quantity
                else:
                    total_cost -= sell_quantity * buy_transaction.price_per_share
                    buy_transaction.quantity -= sell_quantity
                    sell_quantity = 0
                    break

            buy_transactions = [bt for bt in buy_transactions if bt.quantity > 0]
            balance_quantity -= transaction.quantity

        elif 'SPLIT' in transaction.trade_type :
            split_ratio = [int(x) for x in transaction.trade_type.split(" ")[2].split(':')]
            for buy_transaction in buy_transactions:
                buy_transaction.quantity *= split_ratio[1]
                buy_transaction.price_per_share /= split_ratio[1]
            balance_quantity=balance_quantity*split_ratio[1]
            print(split_ratio,buy_transactions)

    if balance_quantity > 0:
        average_buy_price = round(float(total_cost) / balance_quantity,2)
    else:
        average_buy_price = 0

    return JsonResponse({
        'average_buy_price': average_buy_price,
        'balance_quantity': balance_quantity,
    })