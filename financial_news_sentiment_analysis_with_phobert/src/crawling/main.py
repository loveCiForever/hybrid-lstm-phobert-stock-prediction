# src/crawling/main.py

import time
import pandas as pd
from src.crawling.runner import run
from src.utils import format_text

if __name__ == "__main__":
    start_time = time.time()

    merged_df = run()
    output = "data/raw/dataset.csv"
    merged_df.to_csv(output, index=False, encoding='utf-8-sig')

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(
        format_text(
            text=f"[TIME] Finish crawling news in runtime: {elapsed_time:.2f} seconds",
            fg="cyan",
        )
    )
