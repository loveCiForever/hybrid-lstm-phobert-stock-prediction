# src/matching_parsing/runner.py

import re
import pandas as pd
from src.matching_parsing.matcher import match_all
from src.utils import format_text
from pandas import DataFrame

def split_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text)

def run() -> DataFrame:
    vn30_symbol_list = pd.read_csv("data/raw/vn30_symbol_list.csv")['symbol'].to_list()
    raw_dataset = pd.read_csv("data/raw/dataset.csv")

    results = []

    for idx, row in raw_dataset.iterrows():
        content = row['content']
        mentioned_symbol = match_all(content=content, required_symbol_list=vn30_symbol_list)
        if not mentioned_symbol:
            continue

        publish_date = row['publish_date']
        sentences = split_sentences(content)

        for symbol in mentioned_symbol:
            for i, sentence in enumerate(sentences):
                if symbol in sentence:
                    prev_sentence = sentences[i-1] if i > 0 else ""
                    next_sentence = sentences[i+1] if i < len(sentences) - 1 else ""
                    context = " ".join([prev_sentence, sentence, next_sentence]).strip()

                    if len(context) > 256:
                        context = " ".join([prev_sentence, sentence]).strip()
                    if len(context) > 256:
                        context = sentence.strip()

                    num_sentences = len(split_sentences(context))
                    results.append({
                        "original_id": idx,
                        "symbol": symbol,
                        "context": context,
                        "len": len(context),
                        "publish_date": publish_date,
                        "num_sentences": num_sentences
                    })

    df_result = pd.DataFrame(results)
    return df_result