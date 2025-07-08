# src/labeling/runner.py

import pandas as pd
from datetime import datetime
from src.labeling.labeler import (
    get_nearest_close_price,
    get_nearest_index,
)
from pandas import DataFrame
import numpy as np

def labeling_run(price_df:str="data/raw/vn30_price_df.csv", index_df:str="data/raw/vn30_index_df.csv", parsed_dataset:str="data/parsed/dataset.csv") -> DataFrame:
    vn30_price_df = pd.read_csv(price_df)
    vn30_index_df = pd.read_csv(index_df)
    parsed_dataset = pd.read_csv(parsed_dataset)

    vn30_price_df['time'] = pd.to_datetime(vn30_price_df['time'], errors='coerce')
    vn30_index_df['time'] = pd.to_datetime(vn30_index_df['time'], errors='coerce')
    parsed_dataset['publish_date'] = pd.to_datetime(parsed_dataset['publish_date'], errors='coerce')

    price_before_list = []
    price_after_list = []
    index_before_list = []
    index_after_list = []
    status_list = []

    for _, row in parsed_dataset.iterrows():
        symbol = row['symbol']
        publish_date = row['publish_date']

        price_before, price_after = get_nearest_close_price(
            price_df=vn30_price_df,
            symbol=symbol,
            target_date=publish_date
        )
        index_before, index_after = get_nearest_index(
            index_df=vn30_index_df,
            target_date=publish_date
        )

        if any(
            x is None or (isinstance(x, float) and np.isnan(x))
            for x in [price_before, price_after, index_before, index_after]
        ):
            status_list.append("miss_info")
        else:
            status_list.append("ok")

        price_before_list.append(price_before)
        price_after_list.append(price_after)
        index_before_list.append(index_before)
        index_after_list.append(index_after)

    parsed_dataset['price_before'] = price_before_list
    parsed_dataset['price_after'] = price_after_list
    parsed_dataset['index_before'] = index_before_list
    parsed_dataset['index_after'] = index_after_list
    parsed_dataset['status'] = status_list

    for col in ['num_sentences', 'original_id', 'len', 'context']:
        if col in parsed_dataset.columns:
            parsed_dataset = parsed_dataset.drop(columns=[col])

    return parsed_dataset

