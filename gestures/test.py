import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

base_options = python.BaseOptions(model_asset_path='gestures/hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options,
                                       num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

image = mp.Image.create_from_file("gestures/original_images/fist/033_color.png")

detection_result = detector.detect(image)

print(detection_result.hand_landmarks)
# print(detection_result.hand_world_landmarks)