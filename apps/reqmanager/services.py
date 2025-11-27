import requests
import aiohttp

import asyncio
from django.utils import timezone
from .models import BitcoinUsd


async def fetch_price(session):
    url = "https://api.binance.com/api/v3/ticker/price"
    params = {"symbol":"BTCUSD"}



async def update_prices():
    async with aiohttp.ClientSession() as session:
        while True:
            price = await fetch_price(session)
            BitcoinUsd.objects.create(
                price=price,
                symbol="BTCUSD",
                timestamp=timezone.now()

            )


            points = BitcoinUsd.objects.filter(symbol="BTCUSD").order_by('-timestamp')
            if points.count() >24:
                for i in points[24]:
                    i.delete()
            
            await asyncio.sleep(5)


