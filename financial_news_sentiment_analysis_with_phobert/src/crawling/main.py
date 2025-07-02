# src/crawling/main.py

import time
import pandas as pd
from src.crawling.runner import crawling
from src.utils import format_text

if __name__ == "__main__":
    start_time = time.time()

    site_1 = "bao_dau_tu"
    news_details_list_1 = crawling(verbose=False, max_page=100, site=site_1)
    df_1 = pd.DataFrame(news_details_list_1)
    df_1['source'] = site_1

    site_2 = "cafef"
    news_details_list_2 = crawling(verbose=False, max_page=100, site=site_2)
    df_2 = pd.DataFrame(news_details_list_2)
    df_2['source'] = site_2

    merged_df = pd.concat([df_1, df_2], ignore_index=True)
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

    print(
        format_text(
            text=f"[SUCCESS] Saved total {len(merged_df)} news to {output}",
            fg="green",
            style="bold"
        )
    )