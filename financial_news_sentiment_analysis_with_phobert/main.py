# main.py

import pandas as pd
from src.crawling.runner import crawling_run
import time
from src.utils import format_text
from src.preprocessing.runner import matching_parsing_run

# def under_sample_labels(input_csv, output_csv, label_col='trend', n_samples_dict=None, random_state=42):
#     df = pd.read_csv(input_csv)
#     df = df[df[label_col] != 'miss info']
#     df[label_col] = df[label_col].astype(int)
#     if n_samples_dict is None:
#         raise ValueError(f"n_samples_dict must be provided, ví dụ: {0: 10000, 1: 20000, 2: 15000}")
#     dfs = []
#     for label, n_samples in n_samples_dict.items():
#         df_label = df[df[label_col] == label]
#         sample_n = min(len(df_label), n_samples)
#         dfs.append(df_label.sample(n=sample_n, random_state=random_state))
#     df_under_sampled = pd.concat(dfs).reset_index(drop=True)
#     df_under_sampled.to_csv(output_csv, index=False, encoding='utf-8-sig')
#     print(f"save to {output_csv}")

# under_sample_labels(
#     input_csv="data/labeled/dataset.csv",
#     output_csv="data/balanced/dataset_1k_1k_1k.csv",
#     n_samples_dict={0: 1000, 1: 1000, 2: 1000}
# )


if __name__ == "__main__":
    start_time = time.time()

    merged_df = crawling_run(bao_dau_tu_max_page=1, cafef_max_page=1)
    output = "data/raw/test.csv"
    merged_df.to_csv(output, index=False, encoding='utf-8-sig')

    matched_parsed_context = matching_parsing_run(input_path="data/raw/test.csv")

    print(matched_parsed_context.sample(10).iloc[0])

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(
        format_text(
            text=f"[TIME] Finish all process in runtime: {elapsed_time:.2f} seconds",
            fg="cyan",
            style="blink"
        )
    )