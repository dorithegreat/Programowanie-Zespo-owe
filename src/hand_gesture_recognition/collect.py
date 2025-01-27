import cv2
import mediapipe as mp
import numpy as np
import os

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


def save_gesture_data(gesture_name, data, save_path="gesture_data"):
    os.makedirs(save_path, exist_ok=True)
    gesture_path = os.path.join(save_path, f"{gesture_name}.npy")
    if os.path.exists(gesture_path):
        existing_data = np.load(gesture_path, allow_pickle=True)
        data = np.concatenate((existing_data, data), axis=0)
    np.save(gesture_path, data)
    print(f"Zapisano {len(data)} przykładów do {gesture_path}")

def collect_data():
    cap = cv2.VideoCapture(0)

    print("Podaj nazwę gestu, który chcesz zbierać:")
    gesture_name = input("Nazwa gestu: ").strip()
    data = []

    with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
    ) as hands:

        while True:
            success, img = cap.read()
            if not success:
                print("Nie udało się uzyskać obrazu z kamery.")
                break

            img = cv2.flip(img, 1)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)

            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                lm_list = []

                for lm in hand_landmarks.landmark:
                    lm_list.extend([lm.x, lm.y, lm.z])

                data.append(lm_list)

                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            cv2.putText(img, f"Zbieranie gestu: {gesture_name}",
                        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.imshow("Zbieranie danych gestu", img)

            key = cv2.waitKey(1)
            if key == ord('q'):  # 'q', aby zakończyć zbieranie danych
                break

    cap.release()
    cv2.destroyAllWindows()

    if data:
        save_gesture_data(gesture_name, np.array(data))
