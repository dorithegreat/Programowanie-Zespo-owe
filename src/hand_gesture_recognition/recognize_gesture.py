import argparse
import cv2
import mediapipe as mp

# Konfiguracja MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


# Funkcja do uzyskiwania argumentów
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
                        type=float,  # Changed to float for consistency
                        default=0.5)
    args = parser.parse_args()

    return args


# Główna funkcja
def main():
    args = get_args()

    # Ustawienia kamery
    cap = cv2.VideoCapture(args.device)
    cap.set(3, args.width)
    cap.set(4, args.height)

    # Inicjalizacja detektora dłoni MediaPipe
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

            # Odbicie obrazu w poziomie
            img = cv2.flip(img, 1)

            # Konwersja obrazu do RGB dla MediaPipe
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)

            # Przetwarzanie wyników i wyświetlanie punktów orientacyjnych
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Rysowanie punktów orientacyjnych na obrazie
                    mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Uzyskiwanie i wyświetlanie współrzędnych punktów orientacyjnych
                    lm_list = []
                    for id, lm in enumerate(hand_landmarks.landmark):
                        h, w, _ = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lm_list.append((cx, cy))
                        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

                    print("Landmark points:", lm_list)

            # Wyświetlanie obrazu z naniesionymi punktami orientacyjnymi
            cv2.imshow('Image', img)
            key = cv2.waitKey(1)
            if key == 27:  # Wyjście po naciśnięciu ESC
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
