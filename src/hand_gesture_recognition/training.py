import pandas as pd
import numpy as np
import tensorflow as tf
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def load_data(csv_file):
    data = pd.read_csv(csv_file)
    data.columns = data.columns.str.strip()

    data = data.drop(columns=['empty'], errors='ignore')

    X = data.iloc[:, 1:-1].values
    y = data['gesture_name'].values

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    X = X / np.max(X, axis=0)

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
    X, y, label_encoder = load_data(csv_file)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    num_classes = len(np.unique(y))
    model = build_model(X_train.shape[1], num_classes)

    # Train the model
    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2) # nauka tylko 50 linijek, zwiększyć potem

    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Test Accuracy: {accuracy:.2f}")

    model.save("gesture_recognition_model.keras")
    print("Model saved as gesture_recognition_model.h5")

    np.save("label_encoder_classes.npy", label_encoder.classes_)
    print("Label encoder classes saved as label_encoder_classes.npy")


if __name__ == "__main__":
    main()
