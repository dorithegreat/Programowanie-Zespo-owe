from enum import Enum

<<<<<<< HEAD
=======
# cannot for the life of me figure out how to properly import this
from src.computer_controler_package.computer_controller.input_controller import InputController

# I'm not entirely sure we need these at all
# they were intended for clicking and dragging, and dealing with unreliable gesture recognition
>>>>>>> main
class States(Enum):
    cursor = 1
    left_click = 2
    right_click = 3
    scroll = 4
<<<<<<< HEAD
    # define more states for more gestures and their related functionalities
=======
>>>>>>> main

class GestureProcessor:
    #class fields
    state = 0

<<<<<<< HEAD
    #basically a finite automaton
    #jftt coming in handy
    state_change_table = None
    prev_position = None

    def __init__(self):
        pass
=======


    def __init__(self):
        self.prev_position = None
        self.input_controller = InputController()
>>>>>>> main

    #for now I expect positions to be of type HandLandmarkerResults
    #I intend to eventually change it to something more friendly because fuck the mediapipe documentation
    def process(self, gesture, positions):
<<<<<<< HEAD
        pass
=======
        if gesture == "palm_up":
            self.move_cursor(positions)
        elif gesture == "fist":
            self.left_click(positions)
        elif gesture == "span":
            self.right_click(positions)
        elif gesture == "palm_sideways":
            self.scroll(positions)
>>>>>>> main


    def move_cursor(self, positions):
        #extract wrist data from landmarks
<<<<<<< HEAD
        landmarks = positions.hand_landmarks
        wrist_landmark = landmarks[0][0]
        

        #decide what to send further
        #might need to flip the order in the subtraction depending on further implementation
        x_change = self.prev_postition.x -  wrist_landmark.x
        y_change = self.prev_position.y - wrist_landmark.y
        #z coord is irrelevant for this

        #send(x_change, y_change)

    def left_click(self, positions):
        #extract wrist data as above

        #send(left_click)
        
        #determine if hand is moving and process movement like above

        pass
=======
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

>>>>>>> main

    def scroll(self, positions):
        landmarks = positions.hand_landmarks
        wrist_landmark = landmarks[0][0]

<<<<<<< HEAD
        #determine if the movement is more horizontal or vertical, scroll accordingly
        x_change = self.prev_postition.x -  wrist_landmark.x
        y_change = self.prev_position.y - wrist_landmark.y

        if x_change > y_change:
            #send(scroll, horizontal, x_change)
            pass
        else:
            #send(scroll, vertical, y_change)
            pass
=======
        # I cannot find where in Michał's code is scrolling located, if anywhere

        #determine if the movement is more horizontal or vertical, scroll accordingly
        # x_change = self.prev_postition.x -  wrist_landmark.x
        # y_change = self.prev_position.y - wrist_landmark.y

        
>>>>>>> main

