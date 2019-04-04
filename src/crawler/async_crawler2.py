from collections import namedtuple
import time

import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup

### Market Code
KOSPI = 0
KOSDAQ = 1
###

### Crawl configuration
TIMEOUT = 15
###

### Base URL
TICKER_URL = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok={market}&page={page}"
PRICE_URL = "https://fchart.stock.naver.com/sise.nhn?symbol={symbol}&timeframe={timeframe}&count={count}&requestType=0" 
### 

Stock = namedtuple('Stock', 'market_type name code')


async def get_soup(url):
    timeout = aiohttp.ClientTimeout(total=TIMEOUT)
    async with aiohttp.ClientSession() as sess:
        try:
            async with sess.get(url, headers={'user-agent': 'Mozilla/5.0'}, timeout=timeout) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, "lxml")
                    return soup
        except Exception as e:
            if response is not None:
                response.close()
            raise e
        
        finally:
            if response is not None:
                await response.release()


async def get_stock_information(url, semaphore):
    try:
        bucket = []
        await semaphore.acquire()
        soup = await get_soup(url)
        stock_information = soup.select('table.type_2 td a.tltle')
        for s in stock_information:
            company_name = s.text.replace(';', '')
            code = s['href'].split('=')[-1]
            bucket.append(Stock(market_type=KOSPI, name=company_name, code=code))
    except Exception as e:
        print(e)
    finally:
        semaphore.release()
    return bucket


async def main():
    stock_bucket = []
    semaphore = asyncio.Semaphore(5)
    futures = [asyncio.ensure_future(get_stock_information(TICKER_URL.format(market=KOSPI, page=num), semaphore)) for num in range(1,32)]
    
    for data in asyncio.as_completed(futures):
        bucket = await data
        stock_bucket.extend(bucket)
    return len(stock_bucket)


if __name__ == "__main__":
    try:
        start = time.time()
        loop = asyncio.get_event_loop()
        print("What? ---> ",loop.run_until_complete(main()))
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
        end = time.time()
        print(f'time taken: {end-start}')