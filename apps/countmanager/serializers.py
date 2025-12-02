from rest_framework import serializers



class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12,decimal_places=2)
    


class TransferSerializer(serializers.Serializer):
    to_account = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=12,decimal_places=2)




class BuyActionSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12,decimal_places=2)
    valute = serializers.CharField(max_length=20)



class SellActionSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12,decimal_places=2)
    valute = serializers.CharField(max_length=20)


