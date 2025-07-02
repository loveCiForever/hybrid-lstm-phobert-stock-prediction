# src/utils.py

import re
import pandas as pd
from datetime import datetime, date
from matplotlib import pyplot as plt
from bs4 import BeautifulSoup

COLORS = {
    'black': 0,'red':1,'green':2,'yellow':3,'blue':4,'magenta':5,'cyan':6,'white':7,'default':9
}
STYLES = {'bold':1,'dim':2,'underline':4,'blink':5,'reverse':7,'hidden':8,'normal':22}


def format_text(text, fg=None, bg=None, style=None):
    colors = {
        "black": 0,
        "red": 1,
        "green": 2,
        "yellow": 3,
        "blue": 4,
        "magenta": 5,
        "cyan": 6,
        "white": 7,
        "default": 9
    }

    styles = {
        "bold": 1,
        "dim": 2,
        "underline": 4,
        "blink": 5,
        "reverse": 7,
        "hidden": 8,
        "normal": 22
    }

    seq = "\033["

    codes = []

    if style in styles:
        codes.append(str(styles[style]))

    if fg in colors:
        codes.append(str(30 + colors[fg]))

    if bg in colors:
        codes.append(str(40 + colors[bg]))

    if not codes:
        return text

    seq += ";".join(codes) + "m" + text + "\033[0m"
    return seq

def parse_date_span_to_datetime(soup: BeautifulSoup) -> datetime:
    cafef_span = soup.find("span", class_="pdate")
    # <span class="pdate" data-role="publishdate">22-06-2025 - 08:48 AM </span>

    bao_dtu_span = soup.find("span", class_="post-time")
    # <span class="post-time"> - 24/06/2025 12:49</span>

    try:
        if cafef_span:
            raw = cafef_span.get_text(strip=True)
            date = raw.split(" ")[0]

            dt = datetime.strptime(f"{date}", "%d-%m-%Y")

            return dt
        elif bao_dtu_span:
            raw = bao_dtu_span.get_text(strip=True)
            date = raw.split(" ")[1]

            date_str = date.replace("/","-")

            dt = datetime.strptime(f"{date_str}", "%d-%m-%Y")

            return dt
    except Exception as e:
        print(
            format_text(
                text=f"Parse publish datetime to date failed: {raw} | {e}",
                fg="red"
            )
        )

    return None