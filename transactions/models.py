from django.db import models

class Transaction(models.Model):
     

    company = models.CharField(max_length=100)
    trade_date = models.DateField()
    trade_type = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price_per_share = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.trade_date} - {self.company} - {self.trade_type} - {self.quantity} - {self.price_per_share}"
