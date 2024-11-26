import pandas as pd
import numpy as np
import tensorflow as tf
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def normalize_data(data, width=960, height=540):
    normalized_data = []

    for i, row in data.iterrows():
        lm_list = []

        for j in range(1, 22):
            x = row[f'x{j}'] / width
            y = row[f'y{j}'] / height
            z = row[f'z{j}']
            lm_list.extend([x, y, z])

        normalized_data.append(lm_list)

    return np.array(normalized_data)


def load_and_preprocess_data(csv_file):
    data = pd.read_csv(csv_file)
    data.columns = data.columns.str.strip()

    data = data.drop(columns=['empty'], errors='ignore')

    X = normalize_data(data)

    y = data['gesture_name'].values
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    return X, y, label_encoder


def build_model(input_shape, num_classes):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_shape=(input_shape,)),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model


def main():
    csv_file = os.path.join("..", "..", "gestures", "data.csv")

    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"Ścieżka {csv_file} jest nie poprawna.")

    X, y, label_encoder = load_and_preprocess_data(csv_file)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    input_shape = X_train.shape[1]
    num_classes = len(np.unique(y))
    model = build_model(input_shape, num_classes)

    # amount of epochs to change
    history = model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2)

    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Test Accuracy: {accuracy:.2f}")

    model.save("gesture_recognition_model.keras")
    np.save("label_encoder_classes.npy", label_encoder.classes_)


if __name__ == "__main__":
    main()
