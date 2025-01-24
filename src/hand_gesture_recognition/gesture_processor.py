from enum import Enum

class States(Enum):
    cursor = 1
    left_click = 2
    right_click = 3
    scroll = 4
    # define more states for more gestures and their related functionalities

class GestureProcessor:
    #class fields
    state = 0

    #basically a finite automaton
    #jftt coming in handy
    state_change_table = None
    prev_position = None

    def __init__(self):
        pass

    #for now I expect positions to be of type HandLandmarkerResults
    #I intend to eventually change it to something more friendly because fuck the mediapipe documentation
    def process(self, gesture, positions):
        pass


    def move_cursor(self, positions):
        #extract wrist data from landmarks
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

    def scroll(self, positions):
        landmarks = positions.hand_landmarks
        wrist_landmark = landmarks[0][0]

        #determine if the movement is more horizontal or vertical, scroll accordingly
        x_change = self.prev_postition.x -  wrist_landmark.x
        y_change = self.prev_position.y - wrist_landmark.y

        if x_change > y_change:
            #send(scroll, horizontal, x_change)
            pass
        else:
            #send(scroll, vertical, y_change)
            pass

