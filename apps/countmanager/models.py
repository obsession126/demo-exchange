from django.db import models
from users.models import CustomUser



class Account(models.Model):
    user = models.Model(CustomUser,on_delete =models.CASCADE)
    balance  = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    currency = models.CharField(max_length=3,default='USD')


    def __str__(self):
        return f"{self.user.email} - {self.balance} {self.currency}"
    





class Transaction(models.Model):
    TYPE_CHOICES = [
        ("DEPOSIT","Deposit"),
        ("TRANSFER","Transfer"),
                ]
    

    account = models.ForeignKey(Account,on_delete=models.CASCADE,related_name="transactions")
    amount = models.DecimalField(max_digits=12,decimal_places=2)
    type = models.CharField(max_length=10,choices=TYPE_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)


    to_accounts = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True,blank=True,related_name="transfers")


    class Meta:
        ordering = ['-created'] 


        