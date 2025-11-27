from django.db import models


class BitcoinUsd(models.Model):
    price = models.DecimalField()
    symbol = models.CharField(max_length=100)
    timestamp = models.DateTimeField()

