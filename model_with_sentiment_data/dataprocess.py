import pandas as pd
import numpy as np

def prepare_data(filepath, lags=[1, 5, 10, 20]):
    df = pd.read_csv(filepath)

    df["log_return"] = np.log(df["close"] / df["close"].shift(1))

    df["sentiment_score"] = df["prob_positive"] - df["prob_negative"]
    df["sentiment_strength"] = df["prob_positive"] + df["prob_negative"]

    for lag in lags:
        df[f"sentiment_score_lag_{lag}"] = df["sentiment_score"].shift(lag)
        df[f"sentiment_strength_lag_{lag}"] = df["sentiment_strength"].shift(lag)

    df["close_shifted_5"] = df["close"].shift(-5)
    df["target_up_5"] = (df["close_shifted_5"] > df["close"]).astype(int)

    df = df.dropna().reset_index(drop=True)

    print(df.head())

    return df
def normalize_data(df,cols):
    df_norm = df.copy()
    for col in cols:
        min_v = df[col].min()
        max_v = df[col].max()
        df_norm[col] = 2 * (df[col] - min_v) / (max_v - min_v) - 1
    return df_norm
if __name__ == "__main__":
    feature_cols = [
        "log_return",
        "sentiment_score",
        "sentiment_strength",
        "sentiment_score_lag_1",
        "sentiment_score_lag_5",
        "sentiment_score_lag_10",
        "sentiment_score_lag_20",
        "sentiment_strength_lag_1",
        "sentiment_strength_lag_5",
        "sentiment_strength_lag_10",
        "sentiment_strength_lag_20"
    ]

    df_normalized = normalize_data(df_processed, feature_cols)

