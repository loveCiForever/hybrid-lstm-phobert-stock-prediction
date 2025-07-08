from src.labeling.runner import labeling_run
from src.labeling.labeler import label_by_price_volatility, label_by_alpha

if __name__ == "__main__":
    a = labeling_run(
        price_df="data/raw/vn30_price_df.csv",
        index_df="data/raw/vn30_index_df.csv",
        parsed_dataset="data/parsed/dataset.csv"
    )
    a = a[a['status'] != "miss_info"].reset_index(drop=True)
    a = label_by_price_volatility(a, threshold=0.01)

    a = label_by_alpha(a, threshold=0.01)

    print(a.info())
    a.to_csv("data/labeled/dataset.csv", index=False, encoding='utf-8-sig')