from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import BNBBalance,BTCBalance,ETHBalance
from .serializers import DepositSerializer, TransferSerializer
from .models import Account, Transaction
from .services import price_request
import asyncio

from users.models import CustomUser
from .serializers import (
    DepositSerializer,
    TransferSerializer,
    BuyActionSerializer,
    SellActionSerializer
)





@api_view(["POST"])
@permission_classes([IsAuthenticated])
def deposite(request):
    ser = DepositSerializer(data=request.data)
    ser.is_valid(raise_exception=True)


    acc = request.user.account
    amount = ser.validated_data["amount"]


    acc.balance +=amount
    acc.save()


    Transaction.objects.create(
        account=acc,
        amount=amount,
        type="DEPOSIT",
        description="Deposit"

    )


    return Response({'balance':acc.balance})





@api_view(["POST"])
@permission_classes([IsAuthenticated])
def transfer(request):
    ser = TransferSerializer(data=request.data)
    ser.is_valid(raise_exception=True)


    amount = ser.validated_data["amount"]
    to_id = ser.validated_data["to_account_id"]
    

    from_acc = request.user.account
    to_acc = Account.objects.get(id=to_id)


    if from_acc.id == to_acc.id:
        return Response({"error":"You cant do this!!!"},status=400)
    

    if from_acc.balance <amount:
        return Response({"error":"You dont have money for this transaction!!!"},status=400)
    


    from_acc.balance -=amount
    from_acc.save()


    to_acc.balance += amount 
    to_acc.save()


    Transaction.objects.create(
        account=from_acc,
        to_accounts=to_acc,
        amount=amount,
        type="TRANSFER",
        description=f"Transactions to {to_acc.id}"
    )

    return Response({"balance":from_acc.balance})






@api_view(["POST"])
@permission_classes([IsAuthenticated])
def bye_action(request):
    ser = BuyActionSerializer(data=request.data)
    ser.is_valid(raise_exception=True)


    amount = ser.validated_data["amount"]
    valute = ser.validated_data["valute"]

    account = request.user.account
    SYMBOLS = {
    "BTCUSDT": BTCBalance,
    "ETHUSDT": ETHBalance,
    "BNBUSDT": BNBBalance
        }

    if valute not in SYMBOLS:
        return Response({"error": "Unknown currency"}, status=400)
    
    model = SYMBOLS[valute]


    slot, _ = model.objects.get_or_create(user=account)
    if slot.is_active:
        if account.balance < amount:
            return Response({"error":"You dont have money for this transaction!!!"},status=400)
                
        try:
            price = asyncio.run(price_request(symbol_name=valute))
            result_price = amount/price

                    
            slot.balance += result_price

            account.balance-=amount
            

                    

            Transaction.objects.create(
                account=account,
                amount=amount,
                type="BUY_ACTION",
                description=f"Transactions from {account.id} to buy {amount} {valute}"
                )
                    
            slot.save()
            account.save()
            return Response({"balance": account.balance})
        except:
            return Response({"error":"Error"},status=400)


    else:
        return Response({"error":"This slot is inactive"},status=400)

            



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def sell_action(request):
    ser = SellActionSerializer(data=request.data)
    ser.is_valid(raise_exception=True)


    amount = ser.validated_data["amount"]
    valute = ser.validated_data["valute"]


    account = request.user.account
    SYMBOLS = {
    "BTCUSDT": BTCBalance,
    "ETHUSDT": ETHBalance,
    "BNBUSDT": BNBBalance
}

    if valute not in SYMBOLS:
        return Response({"error": "Unknown currency"}, status=400)
    

    model = SYMBOLS[valute]
    slot, _ = model.objects.get_or_create(user=account)

    if slot.balance >= amount:
        try:
            price = asyncio.run(price_request(symbol_name=valute))
                    
            user_money = amount*price

            account.balance += user_money
            slot.balance -= amount


            Transaction.objects.create(
                    account=account,
                    amount=user_money,
                    type="SELL_ACTION",
                    description=f"Transactions from {account.id} to sell {amount} {valute}"
                    )
                        
            slot.save()
            account.save() 
            return Response({"balance": account.balance})
        except:
            return Response({"error":"Error"},status=400)
                


    else:
        return Response({"error":"You havent this valute in this quantity."},status=400)

