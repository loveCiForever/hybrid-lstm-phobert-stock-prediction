import pandas as pd
import numpy as np
import os
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
import tensorflow as tf
import matplotlib.pyplot as plt

df = pd.read_csv("new_data.csv")
output_dir: str = "output",
lookback: int = 20,
epochs: int = 20,
batch_size: int = 4
os.makedirs(output_dir, exist_ok=True)

df["time"] = pd.to_datetime(df["time"])
df = df.sort_values("time").reset_index(drop=True)

data = df[["open", "high", "low", "close", "volume"]].values

scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)

X, y = [], []
for i in range(lookback, len(scaled_data)):
    X.append(scaled_data[i-lookback:i])
    y.append(scaled_data[i][3])  # giá đóng cửa
X = np.array(X)
y = np.array(y)

print(f"Total samples: {len(X)}")

X_train = X[:-20]
X_test = X[-20:]
y_train = y[:-20]
y_test = y[-20:]

print(f"🔹 Train samples: {len(X_train)}")
print(f"🔹 Test samples: {len(X_test)}")

gpus = tf.config.list_physical_devices('GPU')
device = '/GPU:0' if gpus else '/CPU:0'
print(f"Using device: {device}")

with tf.device(device):
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(lookback, 5)),
        LSTM(50),
        Dense(1)
    ])
    model.compile(optimizer="adam", loss="mean_squared_error")

    early_stop = EarlyStopping(monitor="loss", patience=3, restore_best_weights=True)

    history = model.fit(
        X_train, y_train,
        epochs=epochs,
        batch_size=batch_size,
        callbacks=[early_stop],
        verbose=1
    )

# Dự đoán train
y_pred_train_scaled = model.predict(X_train)
y_pred_test_scaled = model.predict(X_test)

def inverse_close(scaled_close):
    dummy = np.zeros((len(scaled_close), scaled_data.shape[1]))
    dummy[:, 3] = scaled_close[:, 0]
    return scaler.inverse_transform(dummy)[:, 3]

y_train_pred = inverse_close(y_pred_train_scaled)
y_test_pred = inverse_close(y_pred_test_scaled)

y_train_true = inverse_close(y_train.reshape(-1, 1))
y_test_true = inverse_close(y_test.reshape(-1, 1))

# Metrics
train_rmse = np.sqrt(mean_squared_error(y_train_true, y_train_pred))
train_mae = mean_absolute_error(y_train_true, y_train_pred)

test_rmse = np.sqrt(mean_squared_error(y_test_true, y_test_pred))
test_mae = mean_absolute_error(y_test_true, y_test_pred)

print(f"Train evaluation:")
print(f"   RMSE: {train_rmse:.4f}")
print(f"   MAE: {train_mae:.4f}")

print(f"Test evaluation:")
print(f"   RMSE: {test_rmse:.4f}")
print(f"   MAE: {test_mae:.4f}")

# Save model & scaler
model.save(os.path.join(output_dir, "lstm_stock_model.h5"))
np.save(os.path.join(output_dir, "scaler_min.npy"), scaler.min_)
np.save(os.path.join(output_dir, "scaler_scale.npy"), scaler.scale_)
plt.figure(figsize=(12,5))
plt.plot(y_test_true, label="Thực tế (Test)")
plt.plot(y_test_pred, label="Dự đoán (Test)")
plt.title("Giá đóng cửa thực tế vs dự đoán (Test set) - không có dữ liệu cảm xúc")
plt.xlabel("Mẫu")
plt.ylabel("Giá đóng cửa")
plt.legend()
plt.show()
# Save results
results_df = pd.DataFrame({
    "y_true": y_test_true,
    "y_pred": y_test_pred
})
results_path = os.path.join(output_dir, "test_predictions.csv")
results_df.to_csv(results_path, index=False, encoding="utf-8-sig")


