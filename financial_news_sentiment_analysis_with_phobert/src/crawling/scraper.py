# src/crawling/scraper.py

from bs4 import BeautifulSoup
from datetime import datetime
from src.crawling.fetcher import fetch_raw_page
from src.utils import (
    format_text,
    parse_date_span_to_datetime
)
from src.crawling.cleaner import (
    remove_quotes_and_ellipsis,
    remove_photo_captions_and_flatten,
    remove_hex_codes_and_invisible_unicode
)
def scrape_news_url(verbose:bool, site:str, max_pages:int) -> list:
    target_component = None
    target_tag = None

    print(
        format_text(
            text=f"[START] Scraping news url from {site}",
            fg="blue",
        )
    )

    if site == None:
        print(
            format_text(
                text=f"[ERROR] site are required. Support cafef and bao_dtu",
                fg="red"
            )
        )
        return
    elif site == "cafef":
        if max_pages is None:
            max_pages = 5000

        target_component = ".tlitem"
        target_tag = "h3 a[href]"

    elif site == "bao_dau_tu":
        if max_pages is None:
            max_pages = 778

        target_component = ".list_news_home article"
        target_tag = "div.desc_list_news_home a.fs22.fbold[href]"

    all_news = []
    for page in range(1, max_pages + 1):
        try:
            api_url = None
            if site == "cafef":
                api_url = f"https://cafef.vn/timelinelist/18831/{page}.chn"
            elif site == "bao_dau_tu":
                api_url = f"https://baodautu.vn/tai-chinh-chung-khoan-d6/p{page}"

            raw_page = fetch_raw_page(api_url)
            soup = BeautifulSoup(raw_page, "lxml")
            page_news = [] # store news of page

            for div in soup.select(target_component):
                a = div.select_one(target_tag)

                if not a: #skip anchor without url
                    continue

                if site == "cafef":
                    link = f"https://cafef.vn{a['href']}"
                elif site == "bao_dau_tu":
                    link = a['href']

                page_news.append(link)

            if not page_news:
                print(
                    format_text(
                        text=f"No more news at page {page}, stopping",
                        fg="yellow"
                    )
                )
                break

            all_news.extend(page_news)
        except Exception as e:
            print(
                format_text(
                    text=f"Failed to fetch page {page}: {e}",
                    fg="red"
                )
            )
            break

    print(
        format_text(
            text=f"[END] Scraping news list success with total: {len(all_news)} news from {site}",
            fg="magenta",
        )
    )

    return all_news

def scrape_news_details(url:str, verbose:bool, site:str) -> tuple[datetime, str]:
    raw_page = fetch_raw_page(url=url)
    if raw_page is None:
        print(
            format_text(
                text=f"[SKIP] Cannot fetch url: {url}",
                fg="yellow"
            )
        )
        return None, None

    soup = BeautifulSoup(raw_page, "lxml")
    publish_datetime = parse_date_span_to_datetime(soup)
    body = None
    if site == "cafef":
        body = soup.find("div", class_="detail-content")
        if not body:
            print(
                format_text(
                    text=f"[ERROR] Empty body: {url}",
                    fg="red",
                    bg=None,
                    style=None
                )
            )

            return None, None
    elif site == "bao_dau_tu":
        body = soup.find("div", id="content_detail_news")
        if not body:
            print(
                format_text(
                    text=f"[ERROR] Empty body: {url}",
                    fg="red",
                    bg=None,
                    style=None
                )
            )

            return None, None
    paragraphs = []
    for p in body.find_all("p"):
        p_class = p.get("class", [])

        if "author" in p_class: # skip author tag
            continue

        text = p.get_text(separator=' ', strip=True) # prevent sticky text

        if text:
            paragraphs.append(text)

    content = " ".join(paragraphs)
    content = remove_quotes_and_ellipsis(content)
    content = remove_hex_codes_and_invisible_unicode(content)
    content = remove_photo_captions_and_flatten(content)

    return publish_datetime, content