from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController
from src.computer_controller.log import get_logger
from typing import Tuple
import time
#import tkinter as tk



class InputController:
    _instance = None  # Singleton instance

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance of InputController is created."""
        if cls._instance is None:
            cls._instance = super(InputController, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the Singleton instance."""
        if self._initialized:
            return

        # Initialize mouse and keyboard controllers
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.logger = get_logger(__name__)
        self._initialized = True

    def move_cursor_to(self, x: int, y: int):
        """
        Move the cursor to a specific position on the screen.
        :param x: The x-coordinate of the target position.
        :param y: The y-coordinate of the target position.
        """

        #root = tk.Tk()
        #width = root.winfo_screenwidth()  # Szerokość ekranu
        #height = root.winfo_screenheight()  # Wysokość ekranu

        #print(f"Szerokość ekranu: {width}, Wysokość ekranu: {height}")
        #x = min(max(x, 0), width)
        #y = min(max(y, 0), height)

        self.mouse.position = (x, y)
        self.logger.info(f"Moved cursor to ({x}, {y})")

    def move_cursor_gradually(self, start: Tuple[int, int], end: Tuple[int, int], duration: float = 1.0):
        """
        Move the cursor gradually from the start position to the end position using a Bézier curve.
        :param start: The starting position as a tuple (x, y).
        :param end: The ending position as a tuple (x, y).
        :param duration: The duration of the movement in seconds.
        """
        # Calculate control points for the Bézier curve
        control1 = (start[0] + (end[0] - start[0]) * 0.25, start[1] + (end[1] - start[1]) * 0.75)
        control2 = (start[0] + (end[0] - start[0]) * 0.75, start[1] + (end[1] - start[1]) * 0.25)

        # Calculate the number of steps based on the duration
        steps = int(duration * 100)  # 100 steps per second
        for i in range(steps + 1):
            t = i / steps
            # Bézier curve formula
            x = (1 - t) ** 3 * start[0] + 3 * (1 - t) ** 2 * t * control1[0] + 3 * (1 - t) * t ** 2 * control2[0] + t ** 3 * end[0]
            y = (1 - t) ** 3 * start[1] + 3 * (1 - t) ** 2 * t * control1[1] + 3 * (1 - t) * t ** 2 * control2[1] + t ** 3 * end[1]
            self.move_cursor_to(int(x), int(y))
            time.sleep(duration / steps)

        self.logger.info(f"Moved cursor gradually from {start} to {end} in {duration} seconds")

    def write_text(self, text: str, delay: float = 0.1):
        """
        Simulate typing the given text using the keyboard.
        :param text: The text to type.
        :param delay: The delay between keystrokes in seconds.
        """
        for char in text:
            self.keyboard.type(char)
            time.sleep(delay)
        self.logger.info(f"Typed text: '{text}'")

    def get_cursor_position(self) -> Tuple[int, int]:
        """
        Get the current cursor position.
        :return: A tuple (x, y) representing the current cursor position.
        """
        x, y = self.mouse.position
        self.logger.info(f"Current cursor position: ({x}, {y})")
        return (x, y)


    def click(self, left=True):
        """
        Simulate mouse button click.
        """
        if left:
            self.mouse.click(Button.left)
            self.logger.info("Left mouse button clicked")
            return
        
        self.mouse.click(Button.right)
        self.logger.info("Right mouse button clicked")


# Example usage
if __name__ == "__main__":
    # Create a singleton instance of InputController
    input_controller = InputController()

    # Get the current cursor position
    position = input_controller.get_cursor_position()
    print(f"Cursor is at: {position}")

    # Move the cursor to a specific position
    input_controller.move_cursor_to(500, 500)

    # Move the cursor gradually from one position to another
    input_controller.move_cursor_gradually((500, 500), (1000, 1000), duration=0.75)

    # Simulate typing text
    #input_controller.write_text("Hello, World!", delay=0.1)

    # Get the cursor position again
    new_position = input_controller.get_cursor_position()
    print(f"Cursor is now at: {new_position}")