import pandas as pd
import numpy as np
import csv
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
import os

df = pd.read_csv("dataset.csv")

epochs = 20
batch_size = 4

feature_cols = [
    "open","high","low","close","volume",
    "prob_positive","prob_negative","prob_neutral","log_return",
    "sentiment_score","sentiment_strength",
    "sentiment_score_lag_1","sentiment_strength_lag_1",
    "sentiment_score_lag_5","sentiment_strength_lag_5",
    "sentiment_score_lag_10","sentiment_strength_lag_10",
    "sentiment_score_lag_20","sentiment_strength_lag_20",
    "close_shifted_5","target_up_5"
]

target_col = "close"

scaler_features = MinMaxScaler()
scaled_features = scaler_features.fit_transform(df[feature_cols])

scaler_target = MinMaxScaler()
scaled_target = scaler_target.fit_transform(df[[target_col]])

lookback = 20

X, y = [], []
for i in range(lookback, len(df)):
    X.append(scaled_features[i - lookback:i])
    y.append(scaled_target[i])

X, y = np.array(X), np.array(y)

print("Dữ liệu sẵn sàng")
print("X shape:", X.shape)
print("y shape:", y.shape)
X_train = X[:-20]
X_test = X[-20:]
y_train = y[:-20]
y_test = y[-20:]
print(f"🔹 Train samples: {len(X_train)}")
print(f"🔹 Test samples: {len(X_test)}")

model = Sequential([
    LSTM(64, input_shape=(lookback, X.shape[2]), return_sequences=False),
    Dropout(0.2),
    Dense(32, activation="relu"),
    Dense(1)
])

model.compile(optimizer="adam", loss="mse", metrics=["mae"])

history = model.fit(
    X_train, y_train,
    epochs=epochs,
    batch_size=batch_size,
    validation_data=(X_test, y_test),
    verbose=1
)

y_pred_train_scaled = model.predict(X_train)
y_pred_test_scaled = model.predict(X_test)

y_pred_train = scaler_target.inverse_transform(y_pred_train_scaled)
y_true_train = scaler_target.inverse_transform(y_train)

y_pred_test = scaler_target.inverse_transform(y_pred_test_scaled)
y_true_test = scaler_target.inverse_transform(y_test)

train_rmse = np.sqrt(mean_squared_error(y_true_train, y_pred_train))
train_mae = mean_absolute_error(y_true_train, y_pred_train)

test_rmse = np.sqrt(mean_squared_error(y_true_test, y_pred_test))
test_mae = mean_absolute_error(y_true_test, y_pred_test)

print("Kết quả train:")
print("RMSE:", train_rmse)
print("MAE:", train_mae)

print("Kết quả test:")
print("RMSE:", test_rmse)
print("MAE:", test_mae)
output_dir = "output"
results_df = pd.DataFrame({
    "y_true": y_true_test.ravel(),
    "y_pred": y_pred_test.ravel()
})
results_path = os.path.join(output_dir, "test_predictions.csv")
results_df.to_csv(results_path, index=False, encoding="utf-8-sig")
model.save(os.path.join(output_dir, "lstm_stock_model.h5"))
np.save(os.path.join(output_dir, "scaler_min.npy"), scaler_features.min_)
np.save(os.path.join(output_dir, "scaler_scale.npy"), scaler_features.scale_)
# Biểu đồ
plt.figure(figsize=(12,5))
plt.plot(y_true_test, label="Thực tế (Test)")
plt.plot(y_pred_test, label="Dự đoán (Test)")
plt.title("Giá đóng cửa thực tế vs dự đoán (Test set) - có dữ liệu cảm xúc")
plt.xlabel("Mẫu")
plt.ylabel("Giá đóng cửa")
plt.legend()
plt.show()
