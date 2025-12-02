import aiohttp
import asyncio


async def price_request(symbol_name):
    url = "https://api.binance.com/api/v3/ticker/price"
    params = {"symbol":symbol_name}
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url,params=params) as response:
            data = await response.json()
            price = float(data["price"])
            return price 
        

    
