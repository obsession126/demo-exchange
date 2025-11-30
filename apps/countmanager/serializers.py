from rest_framework import serializers



class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12,decimal_places=2)




class TransferSerializer(serializers.Serializer):
    to_account = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=12,decimal_places=2)



    