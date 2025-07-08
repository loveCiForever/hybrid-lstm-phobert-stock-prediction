# src/matching_parsing/runner.py

import re
import pandas as pd
from src.preprocessing.matcher import match_all
from pandas import DataFrame
from src.preprocessing.cleaner import clean_text
from src.preprocessing.parser import split_sentences
from src.preprocessing.segmenter import segment_texts

def preprocessing_run(
    symbol_df_path:str="data/raw/vn30_symbol_df.csv",
    raw_dataset_path:str="data/raw/dataset.csv"
) -> DataFrame:

    vn30_symbol_list = pd.read_csv(symbol_df_path)['symbol'].to_list()
    raw_dataset = pd.read_csv(raw_dataset_path)
    raw_dataset['publish_date'] = pd.to_datetime(raw_dataset['publish_date'], errors='coerce')

    results = []

    for idx, row in raw_dataset.iterrows():
        if row['publish_date'] < pd.Timestamp("2017-08-24"):
            continue

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

                    if len(context) > 250:
                        context = " ".join([prev_sentence, sentence]).strip()
                    if len(context) > 250:
                        context = sentence.strip()

                    context = clean_text(context)

                    if len(context) > 250 or len(context) < 100:
                        continue

                    results.append({
                        "symbol": symbol,
                        "context": context,
                        "publish_date": publish_date,
                    })

    df_result = pd.DataFrame(results)

    if not df_result.empty:
        df_result["context_segmented"] = segment_texts(
            df_result["context"].tolist()
        )

    return df_result