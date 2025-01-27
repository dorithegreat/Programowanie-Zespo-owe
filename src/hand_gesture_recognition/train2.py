import os

import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import resample
from tensorflow.keras.callbacks import EarlyStopping

def load_data(data_path="gesture_data"):
    X, y = [], []
    for file in os.listdir(data_path):
        if file.endswith(".npy"):
            gesture_name = file.split(".npy")[0]
            data = np.load(os.path.join(data_path, file), allow_pickle=True)
            X.extend(data)
            y.extend([gesture_name] * len(data))

    X = np.array(X, dtype=np.float32)
    y = np.array(y)
    return X, y

def balance_data(X, y):
    unique_classes, class_counts = np.unique(y, return_counts=True)
    max_samples = max(class_counts)

    X_balanced, y_balanced = [], []

    for cls in unique_classes:
        cls_indices = np.where(y == cls)[0]
        X_cls, y_cls = X[cls_indices], y[cls_indices]

        X_cls_resampled, y_cls_resampled = resample(
            X_cls, y_cls, replace=True, n_samples=max_samples, random_state=42
        )

        X_balanced.extend(X_cls_resampled)
        y_balanced.extend(y_cls_resampled)

    return np.array(X_balanced), np.array(y_balanced)

def train_model():
    data_path = "gesture_data"
    X, y = load_data(data_path)

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    np.save("label_encoder_classes.npy", label_encoder.classes_)

    X_balanced, y_balanced = balance_data(X, y_encoded)

    X_train, X_val, y_train, y_val = train_test_split(X_balanced, y_balanced, test_size=0.2, random_state=42)

    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(X.shape[1],)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(len(label_encoder.classes_), activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=50, batch_size=32, callbacks=[early_stopping])

    model.save("gesture_recognition_model.keras")
    print("Model zapisany jako 'gesture_recognition_model.keras'.")
