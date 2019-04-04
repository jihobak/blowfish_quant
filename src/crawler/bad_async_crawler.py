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


async def get_soup(url):
    async with aiohttp.ClientSession() as sess:
        async with sess.get(url, headers={'user-agent': 'Mozilla/5.0'}) as response:
            html = await response.text()
    
    soup = BeautifulSoup(html, "lxml")
    return soup


async def get_stock_information(url):
    soup = await get_soup(url)
    stock_information = soup.select('table.type_2 td a.tltle')
    for s in stock_information:
        company_name = s.text.replace(';', '')
        code = s['href'].split('=')[-1]
        yield Stock(market_type=KOSPI, name=company_name, code=code)


async def main():
    test_url = TICKER_URL.format(market=KOSPI, page=1)
    stock_bucket = []

    for num in range(1, 32):
        async for s in get_stock_information(TICKER_URL.format(market=KOSPI, page=num)):
            stock_bucket.append(s)
    return len(stock_bucket)


if __name__ == "__main__":
    start = time.time()
    loop = asyncio.get_event_loop()
    print("What? ---> ",loop.run_until_complete(main()))
    loop.close()
    end = time.time()
    print(f'time taken: {end-start}')