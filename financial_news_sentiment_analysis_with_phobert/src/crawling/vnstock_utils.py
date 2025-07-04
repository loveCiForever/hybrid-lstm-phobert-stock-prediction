# src/crawling/vnstock__.py

import pandas as pd
import os
import time
from vnstock import Vnstock
from pandas import DataFrame

stock = Vnstock().stock(symbol='ACB', source='VCI')

def fetch_vn30_symbol_df() -> DataFrame:
    symbols = stock.listing.symbols_by_group("VN30")
    if isinstance(symbols, pd.Series):
        vn30_symbol_df = pd.DataFrame({'symbol': symbols.values})
    else:
        vn30_symbol_df = pd.DataFrame({'symbol': symbols})
    return vn30_symbol_df


def fetch_vn30_price_df(input_path:str = "data/raw/vn30_symbol_df.csv", output_path:str = None) -> DataFrame:
    vn30_symbol_list = []

    if os.path.exists(input_path) == False:
        vn30_symbol_df = fetch_vn30_symbol_df()
        vn30_symbol_df.to_csv(input_path, index=False, encoding="utf-8-sig")
        vn30_symbol_list = vn30_symbol_df['symbol'].to_list()
    else:
        vn30_symbol_df = pd.read_csv(input_path)
        vn30_symbol_list = vn30_symbol_df['symbol'].to_list()

    vn30_price_list = []
    for symbol in vn30_symbol_list:
        symbol_price_df = stock.quote.history(symbol=symbol,start='2000-01-01', end='2026-01-01', interval='1D')
        symbol_price_df['symbol'] = symbol
        vn30_price_list.append(symbol_price_df)
        time.sleep(1)

    vn30_price_df = pd.concat(vn30_price_list, ignore_index=True)

    if output_path:
        vn30_price_df.to_csv(output_path, index=False)

    return vn30_price_df

def fetch_vn30_index() -> DataFrame:
    vn30_index = stock.quote.history(symbol='VN30', start='2000-01-01', end='2026-01-01', interval='1D')

    return vn30_index