# src/crawling/runner.py

from pandas import DataFrame
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.crawling.scraper import (
    scrape_news_details,
    scrape_news_url
)
from src.utils import format_text

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

def run(bao_dau_tu_max_page:int = 10, cafef_max_page:int = 10):
    site_1 = "bao_dau_tu"
    news_details_list_1 = crawling(verbose=False, max_page=bao_dau_tu_max_page, site=site_1)
    df_1 = pd.DataFrame(news_details_list_1)
    df_1['source'] = site_1

    site_2 = "cafef"
    news_details_list_2 = crawling(verbose=False, max_page=cafef_max_page, site=site_2)
    df_2 = pd.DataFrame(news_details_list_2)
    df_2['source'] = site_2

    merged_df = pd.concat([df_1, df_2], ignore_index=True)

    print(
        format_text(
            text=f"[SUCCESS] Found total {len(merged_df)}",
            fg="green",
            style="bold"
        )
    )

    return merged_df