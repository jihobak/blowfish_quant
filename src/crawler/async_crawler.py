from collections import namedtuple
import time

import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup


KOSPI = 0
KOSDAQ = 1

TICKER_URL = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok={market}&page={page}"
PRICE_URL = "https://fchart.stock.naver.com/sise.nhn?symbol={symbol}&timeframe={timeframe}&count={count}&requestType=0" 


Stock = namedtuple('Stock', 'market_type name code')

async def make_soup(url):
    async with aiohttp.ClientSession() as sess:
        async with sess.get(url, headers={'user-agent': 'Mozilla/5.0'}) as response:
            html = await response.text()
    
    soup = BeautifulSoup(html, "lxml")
    return soup


async def main():
    test_url = TICKER_URL.format(market=KOSPI, page=1)
    stock_bucket = []
    futures = [asyncio.ensure_future(make_soup(TICKER_URL.format(market=KOSPI, page=num))) for num in range(1,32)]
    #await asyncio.gather(*futures)
    for f in asyncio.as_completed(futures):
        x = await f
        stock_information = x.select('table.type_2 td a.tltle')
        for sc in stock_information:
            company_name = sc.text.replace(';', '')
            code = sc['href'].split('=')[-1]
            stock_bucket.append(Stock(market_type=KOSPI, name = company_name, code = code))
    print(len(stock_bucket))
    return len(stock_bucket)


if __name__ == "__main__":
    start = time.time()
    loop = asyncio.get_event_loop()
    print("What? ---> ",loop.run_until_complete(main()))
    loop.close()
    end = time.time()
    print(f'time taken: {end-start}')