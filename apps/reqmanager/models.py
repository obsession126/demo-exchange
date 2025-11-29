from django.db import models



class BTCUSDT(models.Model):
    price = models.DecimalField(max_digits=20,decimal_places=8)
    timestamp = models.DateTimeField()



class ETHUSDT(models.Model):
    price = models.DecimalField(max_digits=20,decimal_places=8)
    timestamp = models.DateTimeField()



class BNBUSDT(models.Model):
    price = models.DecimalField(max_digits=20,decimal_places=8)
    timestamp = models.DateTimeField()




