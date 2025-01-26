from enum import Enum

# cannot for the life of me figure out how to properly import this
from src.computer_controler_package.computer_controller.input_controller import InputController

# I'm not entirely sure we need these at all
# they were intended for clicking and dragging, and dealing with unreliable gesture recognition
class States(Enum):
    cursor = 1
    left_click = 2
    right_click = 3
    scroll = 4

class GestureProcessor:
    #class fields
    state = 0



    def __init__(self):
        self.prev_position = None
        self.input_controller = InputController()

    #for now I expect positions to be of type HandLandmarkerResults
    #I intend to eventually change it to something more friendly because fuck the mediapipe documentation
    def process(self, gesture, positions):
        if gesture == "palm_up":
            self.move_cursor(positions)
        elif gesture == "fist":
            self.left_click(positions)
        elif gesture == "span":
            self.right_click(positions)
        elif gesture == "palm_sideways":
            self.scroll(positions)


    def move_cursor(self, positions):
        #extract wrist data from landmarks
        landmarks = positions.multi_hand_landmarks
        wrist_landmark = landmarks[0][0]
        

        #* I think that mouse movement is actually absolute, not relative
        # x_change = self.prev_postition.x -  wrist_landmark.x
        # y_change = self.prev_position.y - wrist_landmark.y
        #z coord is irrelevant for this

        self.input_controller.move_cursor_to(wrist_landmark.x, wrist_landmark.y)

    def left_click(self, positions):

        self.move_cursor(positions)
        
        if self.state == States.left_click:
            # don't click again
            self.input_controller.click(True)
        
        
        
    def right_click(self, positions):
        self.move_cursor(positions)
        
        if self.state == States.left_click:
            # don't click again
            self.input_controller.click(False)


    def scroll(self, positions):
        landmarks = positions.hand_landmarks
        wrist_landmark = landmarks[0][0]

        # I cannot find where in Michał's code is scrolling located, if anywhere

        #determine if the movement is more horizontal or vertical, scroll accordingly
        # x_change = self.prev_postition.x -  wrist_landmark.x
        # y_change = self.prev_position.y - wrist_landmark.y

        

