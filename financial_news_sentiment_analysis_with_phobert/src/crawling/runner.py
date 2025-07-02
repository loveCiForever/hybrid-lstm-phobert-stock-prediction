# src/crawling/runner.py

from pandas import DataFrame
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.crawling.scraper import (
    scrape_news_details,
    scrape_news_url
)

def process_item(url:str, verbose:bool, site:str) -> dict:
    publish_datetime, content = scrape_news_details(
        url=url,
        verbose=verbose,
        site=site
    )

    if not content:
        return None

    return {
        "publish_date": publish_datetime,
        "content": content
    }

def crawling(verbose:bool, max_page:int, site:str) -> list:
    news_url = scrape_news_url(verbose=verbose, site=site, max_pages=max_page)
    news_details = []

    with ThreadPoolExecutor(max_workers=20) as ex:
        futures = [
            ex.submit(
                process_item,
                url,
                verbose,
                site
            ) for url in news_url
        ]
        for f in as_completed(futures):
            r = f.result()
            if r:
                news_details.append(r)

    return news_details