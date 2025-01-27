import argparse
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf

<<<<<<< HEAD
=======
from gesture_processor import GestureProcessor
>>>>>>> main

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", help='cap width', type=int, default=960)
    parser.add_argument("--height", help='cap height', type=int, default=540)
    parser.add_argument('--use_static_image_mode', action='store_true')
    parser.add_argument("--min_detection_confidence",
                        help='min_detection_confidence',
                        type=float,
                        default=0.7)
    parser.add_argument("--min_tracking_confidence",
                        help='min_tracking_confidence',
                        type=float,
                        default=0.5)
    args = parser.parse_args()

    return args


def load_model_and_labels(model_path, label_path):
    model = tf.keras.models.load_model(model_path)
    labels = np.load(label_path, allow_pickle=True)
    return model, labels


def prepare_input_data(hand_landmarks):
    lm_list = []
    for lm in hand_landmarks:
        lm_list.append(lm.x)
        lm_list.append(lm.y)
        lm_list.append(lm.z)

    return lm_list


def main():
    args = get_args()
<<<<<<< HEAD
=======
    
    gesture_processor = GestureProcessor()
>>>>>>> main

    model_path = "gesture_recognition_model.keras"
    label_path = "label_encoder_classes.npy"
    model, labels = load_model_and_labels(model_path, label_path)

    confidence_threshold = 0.7  # Próg pewności

    cap = cv2.VideoCapture(args.device)
    cap.set(3, args.width)
    cap.set(4, args.height)

    with mp_hands.Hands(
            static_image_mode=args.use_static_image_mode,
            max_num_hands=2,
            min_detection_confidence=args.min_detection_confidence,
            min_tracking_confidence=args.min_tracking_confidence
    ) as hands:

        while True:
            success, img = cap.read()
            if not success:
                print("Failed to grab frame.")
                break

            img = cv2.flip(img, 1)

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)

            if results.multi_hand_landmarks:
                lm_list = prepare_input_data(results.multi_hand_landmarks[0].landmark)

                input_data = np.array(lm_list, dtype=np.float32).reshape(1, -1)

                input_data[:, ::3] /= args.width
                input_data[:, 1::3] /= args.height

                prediction = model.predict(input_data)
                predicted_confidence = np.max(prediction)
                predicted_label = labels[np.argmax(prediction)]

                for i, label in enumerate(labels):
                    print(f"Gest: {label}, Prawdopodobieństwo: {prediction[0][i]:.2f}")


                if predicted_confidence >= confidence_threshold:
<<<<<<< HEAD
                    cv2.putText(img, f"Gesture: {predicted_label} ({predicted_confidence:.2f})",
                                (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
=======
                    # cv2.putText(img, f"Gesture: {predicted_label} ({predicted_confidence:.2f})",
                    #             (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                    gesture_processor.process(predicted_label, results)
>>>>>>> main

            cv2.imshow('Gesture Recognition', img)
            key = cv2.waitKey(1)
            if key == 27:  # ESC to quit
                break

    cap.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    main()
