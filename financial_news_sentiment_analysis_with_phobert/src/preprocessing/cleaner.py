# src/matching_parsing/cleaner.py

import re

def clean_text(text:str) -> str:
    text = re.sub(r'^[=\-_*~\s]{3,}$', '', text, flags=re.MULTILINE)
    text = re.sub(r'[=\-_*~]{3,}', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text