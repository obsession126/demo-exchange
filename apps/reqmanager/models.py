from django.db import models


class BitcoinUsd(models.Model):
    price = models.DecimalField(max_digits=20,decimal_places=20)
    symbol = models.CharField(max_length=100)
    timestamp = models.DateTimeField()

