# src/preprocessing/matcher.py

import re

def split_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text)