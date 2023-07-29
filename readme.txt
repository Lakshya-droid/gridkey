1) Activate the virtual env:
    pipenv shell
2) Run the development server:
    python manage.py runserver
    The API will now be accessible at http://localhost:8000/api/.

3) API Endpoints
   GET /api/transactions/: List all transactions.
   POST /api/transations/: to add data to the database:- 
   example - 
   {
  "company": "ABC Ltd.",
  "trade_date": "2018-02-23",
  "trade_type": "BUY",
  "quantity": 100,
  "price_per_share": "100"
  }

4) GET /api/average_buy_price_balance/: Get the average buy price and balance quantity after a specified date.
    http://localhost:8000/api/average_buy_price_balance/?date=23/02/2023

Usage
Use the API endpoints to add new transactions of different types (BUY, SELL, SPLIT).
The API will calculate the average buy price and balance quantity after each transaction based on the FIFO method.
Use the GET /api/average_buy_price_balance/ endpoint to get the average buy price and balance quantity after a specified date.