# src/matching_parsing/matcher.py

import pandas as pd
import re
import os
from src.utils import format_text


def match_all(content: str, required_symbol_list: list) -> list:
    pattern = r'\b(?:' + '|'.join(re.escape(symbol) for symbol in required_symbol_list) + r')\b'
    matched = re.findall(pattern, content)

    return list(set(matched)) if matched else []