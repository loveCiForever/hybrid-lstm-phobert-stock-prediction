# src/labeling/labeler.py

from pandas import DataFrame
from datetime import datetime, timedelta
import pandas as pd

def calculate_alpha(price_before:float, price_after:float, index_before:float, index_after:float) -> float:
    return_stock = (price_after - price_before) / price_before
    return_market = (index_after - index_before) / index_before
    return_alpha = return_stock - return_market

    return return_alpha

def get_nearest_close_price(price_df:DataFrame, symbol: str, target_date: datetime, max_range=10) -> tuple[float, float]:
    symbol_df = price_df[price_df['symbol'] == symbol]

    min_date = target_date - timedelta(days=max_range)
    max_date = target_date + timedelta(days=max_range)

    window_df = symbol_df[
        (symbol_df['time'] >= min_date) &
        (symbol_df['time'] <= max_date)
    ]

    before_df = window_df[window_df['time'] < target_date]
    after_df = window_df[window_df['time'] > target_date]

    before_row = before_df.sort_values('time', ascending=False).head(1)
    after_row = after_df.sort_values('time', ascending=True).head(1)

    price_before = before_row['close'].values[0] if not before_row.empty else None
    price_after = after_row['close'].values[0] if not after_row.empty else None

    return price_before, price_after

def get_nearest_index(index_df: pd.DataFrame, target_date: datetime, max_range=10) -> tuple[float, float]:
    min_date = target_date - timedelta(days=max_range)
    max_date = target_date + timedelta(days=max_range)

    window_df = index_df[
        (index_df['time'] >= min_date) &
        (index_df['time'] <= max_date)
    ]

    before_df = window_df[window_df['time'] < target_date]
    after_df = window_df[window_df['time'] > target_date]

    # print(before_df, after_df)
    before_row = before_df.sort_values('time', ascending=False).head(1)
    after_row = after_df.sort_values('time', ascending=True).head(1)

    index_before = before_row['close'].values[0] if not before_row.empty else None
    index_after = after_row['close'].values[0] if not after_row.empty else None

    return index_before, index_after

import numpy as np

POSITIVE = 0
NEGATIVE = 1
NEUTRAL = 2

def label_by_price_volatility(df, threshold=0.01):
    df_copy = df.copy()
    price_change_pct = (df_copy['price_after'] - df_copy['price_before']) / df_copy['price_before']
    conditions = [
        price_change_pct > threshold,
        price_change_pct < -threshold
    ]
    choices = [POSITIVE, NEGATIVE]
    df_copy['label_vol'] = np.select(conditions, choices, default=NEUTRAL)

    return df_copy

def label_by_alpha(df, threshold=0.01):
    df_copy = df.copy()
    price_change_pct = (df_copy['price_after'] - df_copy['price_before']) / df_copy['price_before']
    index_change_pct = (df_copy['index_after'] - df_copy['index_before']) / df_copy['index_before']
    cond = price_change_pct - index_change_pct

    conditions = [
        cond > threshold,
        cond < -threshold
    ]
    choices = [POSITIVE, NEGATIVE]
    df_copy['label_alpha'] = np.select(conditions, choices, default=NEUTRAL)

    return df_copy