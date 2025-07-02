# src/crawling/fetcher.py

import requests
import time
from src.utils import format_text

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
session = requests.Session()
session.headers.update(HEADERS)

def fetch_raw_page(url:str, retries=3, timeout=10, delay=1) -> str:
    for attempt in range(1, retries + 1):
        try:
            resp = session.get(url, timeout=timeout)
            resp.raise_for_status()

            return resp.text
        except requests.exceptions.RequestException as e:
            print(
                format_text(
                    text=f"[RETRY {attempt}/{retries}] Error fetching {url}: {e}",
                    fg="yellow"
                )
            )
            time.sleep(delay)
    print(
        format_text(
            text=f"[FAILED] Gave up fetching {url} after {retries} retries",
            fg="red"
        )
    )

    return None