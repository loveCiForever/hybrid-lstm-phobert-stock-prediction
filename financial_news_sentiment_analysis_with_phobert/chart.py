import pandas as pd
import matplotlib.pyplot as plt

def draw_source_pie_chart(csv_path):
    df = pd.read_csv(csv_path)
    if 'source' not in df.columns:
        print("No 'source' column found in the CSV.")
        return
    source_counts = df['source'].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(source_counts, labels=source_counts.index, autopct='%1.1f%%', startangle=90, colors=['#4394E5','#9AD8D8'])
    plt.axis('equal')
    plt.show()

def draw_length_distribution(csv_path:str, text_col:str, loc:str):
    df = pd.read_csv(csv_path)
    if text_col not in df.columns:
        print(f"No '{text_col}' column found in the CSV.")
        return
    df['len'] = df[text_col].astype(str).apply(len)
    plt.figure(figsize=(8, 5))
    plt.hist(df['len'], bins=50, color='#4394E5', edgecolor='black')
    avg_len = df['len'].mean()
    plt.axvline(avg_len, color='red', linestyle='dashed', linewidth=2, label=f'Số từ trung bình: {avg_len:.2f}')
    plt.xlabel('Số lượng từ (Word Count)')
    plt.ylabel('Tần suất (Frequency)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(loc=loc, fontsize=10, frameon=True)
    plt.show()

# draw_length_distribution(csv_path="data/labeled/dataset.csv", text_col="context", loc="upper left")
# draw_length_distribution(csv_path="data/raw/dataset.csv", text_col="content", loc="upper right")

def draw_trend_distribution(csv_path: str, trend_col: str = "trend"):

    df = pd.read_csv(csv_path)
    if trend_col not in df.columns:
        print(f"No '{trend_col}' column found in the CSV")
        return

    label_map = {0: "Positive", 1: "Neutral", 2: "Negative"}
    trend_counts = df[trend_col].value_counts().sort_index()
    labels = [label_map.get(i, str(i)) for i in trend_counts.index]

    plt.figure(figsize=(7, 5))
    bars = plt.bar(labels, trend_counts.values, color=['#4394E5'])
    plt.xlabel("Xu hướng (Trend)")
    plt.ylabel("Số lượng mẫu (Volume)")
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 1, int(yval), ha='center', va='bottom', fontsize=11)
    max_y = max(trend_counts.values)
    plt.ylim(top=max_y * 1.15)
    plt.show()

draw_trend_distribution(csv_path="data/labeled/dataset.csv", trend_col = "trend")