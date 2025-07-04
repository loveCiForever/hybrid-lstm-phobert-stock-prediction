# src/crawling/main.py

import time
import pandas as pd
from src.crawling.runner import crawling_run
from src.utils import format_text

if __name__ == "__main__":
    start_time = time.time()

    merged_df = crawling_run(bao_dau_tu_max_page=1, cafef_max_page=1)
    output = "data/raw/test.csv"
    merged_df.to_csv(output, index=False, encoding='utf-8-sig')
    print(merged_df.sample(1).iloc[0])

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(
        format_text(
            text=f"[TIME] Finish crawling news in runtime: {elapsed_time:.2f} seconds",
            fg="cyan",
            style="blink"
        )
    )
