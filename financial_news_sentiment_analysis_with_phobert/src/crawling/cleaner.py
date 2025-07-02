# src/crawling/cleaner.py

import re

def remove_hex_codes_and_invisible_unicode(text:str) -> str:
    """
    Remove hex color codes (e.g., #fff, #ffffff)
        and invisible Unicode characters from the text.
    Also normalizes whitespace.
    """

    # Remove hex color codes
    text = re.sub(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b", '', text)

    # Replace invisible Unicode characters with a space
    text = re.sub(r"[\u200b-\u200d\uFEFF\xa0\u2028]", ' ', text)

    # Collapse multiple spaces into one
    text = re.sub(r"\s+", ' ', text)

    return text.strip()

def remove_photo_captions_and_flatten(text:str) -> str:
    """
    Remove lines starting with 'ẢNH' (case-insensitive)
        and merge all lines into a single line.
    """

    lines = text.split("\n")

    # Remove lines that start with 'ẢNH'
    lines = [l for l in lines if not l.upper().startswith('ẢNH')]

    # Join lines and normalize whitespace
    single = ' '.join(lines)
    single = re.sub(r"\s+", ' ', single)

    return single.strip()


def remove_quotes_and_ellipsis(text:str) -> str:
    """
    Remove surrounding double quotes, replace double double-quotes
        with single double-quotes, and normalize ellipsis
        and similar punctuation to a period.
    """

    # Remove surrounding double quotes
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]

    # Replace double double-quotes with single double-quote
    text = text.replace('""', '"')

    # Replace ellipsis and similar patterns with a period
    text = re.sub(r'…|\.{3}|,\.{2}', '.', text)

    return text