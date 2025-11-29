import time
import requests
from ...models import BTCUSDT,ETHUSDT,BNBUSDT
from django.utils import timezone
from django.core.management.base import BaseCommand
from decimal import Decimal,InvalidOperation
from datetime import datetime


class Command(BaseCommand):

    help = "Parse crypto-price"

    

    def handle(self,*args,**kwargs):
        SYMBOLS = [
            ("BTCUSDT", BTCUSDT),
            ("ETHUSDT", ETHUSDT), 
            ("BNBUSDT", BNBUSDT)
        ]
        price_url = "https://api.binance.com/api/v3/ticker/price"
        klines_url = "https://api.binance.com/api/v3/klines"
        while True:
            for symbol_name, model in SYMBOLS:
                points = model.objects.filter().order_by("-timestamp")

                if len(points)<24:

                    params = {
                        "symbol": symbol_name,
                        "interval": "1h",
                        "limit": 24   
                        }
                    data = requests.get(klines_url, params=params).json()
                    for candle in data:
                        timestamp_ms = candle[0]
                        close_price = candle[4]

                        dt = datetime.fromtimestamp(timestamp_ms / 1000)
                        dt = timezone.make_aware(dt)

                        model.objects.create(
                            price=Decimal(close_price),
                            timestamp=dt
                            )
                        

                params = {"symbol":symbol_name}
                rep = requests.get(url=price_url,params=params)
                data = rep.json()
                try:
                    price_float = float(data["price"])
                    price = Decimal(str(price_float))

                    
                except (ValueError, TypeError, InvalidOperation) as e:
                    print(f"Invalid price for {model}: {data['price']} — {e}")
                    continue  


                model.objects.create(price=Decimal(str(price)),timestamp=timezone.now())

                

                all_points = model.objects.filter().order_by("-timestamp")

                for old in points[24:]:
                    old.delete() 
                        
            print("Prices updated at: ",timezone.now())


            time.sleep(10)