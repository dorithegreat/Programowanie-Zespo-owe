import os
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

def process(file, detector):
    image = mp.Image.create_from_file(file)
    detection_result = detector.detect(image)

    f = open("gestures/first_pass.txt", "a");

    landmarks = detection_result.hand_landmarks
    handednesses = detection_result.handedness


    i = 0
    for normalized_landmark in landmarks:
        l = ""
        l += handednesses[i][0].display_name
        l += ", "
        i += 1

        for element in normalized_landmark:
            l += str(element.x)
            l += ", "
            l += str(element.y)
            l += ", "
            l += str(element.z)
            l += ", "
            l += str(element.visibility)
            l += ", "
            l += str(element.presence)
            l += ", "
        l += ", thumb_down \n"
        f.write(l)

    # print(str(detection_result))



base_options = python.BaseOptions(model_asset_path='gestures/hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options,
                                       num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

for filename in os.listdir('gestures/original_images/thumb_down'):
    process("gestures/original_images/thumb_down/" + filename, detector)

# process("gestures/original_images/fist/033_color.png", detector)