import subprocess as sp
from src.computer_controller.log import get_logger  # Replace 'your_logger_module' with the actual module name


class DisplayController:
    _instance = None  # Singleton instance

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance of DisplayController is created."""
        if cls._instance is None:
            cls._instance = super(DisplayController, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the Singleton instance."""
        if self._initialized:
            return
        self._initialized = True
        self.logger = get_logger("DisplayController")  # Initialize logger
        self.logger.debug("Initializing DisplayController...")
        self.connected_displays = self._get_connected_displays()
        self.logger.info(f"Connected displays: {self.connected_displays}")

    def _get_connected_displays(self):
        """
        Get a list of connected display names using xrandr.
        :return: List of connected display names (e.g., ['eDP-1', 'HDMI-1']).
        """
        self.logger.debug("Retrieving connected displays...")
        result = sp.run(['xrandr', '--query'], capture_output=True, text=True)
        if result.returncode != 0:
            self.logger.error("Error retrieving display information:")
            self.logger.error(result.stderr)
            return []

        # Extract connected displays
        connected_displays = []
        for line in result.stdout.splitlines():
            if ' connected' in line:  # Check if the display is connected
                display_name = line.split()[0]  # The first part is the display name
                connected_displays.append(display_name)
                self.logger.debug(f"Found connected display: {display_name}")
        return connected_displays

    def set_brightness(self, display, brightness_percent):
        """
        Set the brightness of a display using xrandr.
        :param display: Name of the display (e.g., 'eDP-1')
        :param brightness_percent: Brightness level (0 to 100)
        """
        level = max(0.1, min(brightness_percent / 100, 1.0))  # Clamp the value
        self.logger.debug(f"Setting brightness for {display} to {brightness_percent}% (level: {level})")
        sp.run(['xrandr', '--output', display, '--brightness', str(level)])
        self.logger.info(f"Brightness set to {brightness_percent}% for {display}")

    def get_brightness(self, display):
        """
        Get the current brightness of a display.
        :param display: Name of the display (e.g., 'eDP-1')
        :return: Current brightness level (0.1 to 1.0)
        """
        self.logger.debug(f"Retrieving brightness for {display}...")
        result = sp.run(['xrandr', '--verbose'], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if display in line and 'Brightness:' in line:
                current_brightness = float(line.split('Brightness:')[1].strip())
                self.logger.debug(f"Current brightness for {display}: {current_brightness}")
                return current_brightness
        error_msg = f"Display {display} not found or brightness not available."
        self.logger.error(error_msg)
        raise ValueError(error_msg)

    def change_brightness(self, step):
        """
        Adjust the brightness of all connected displays by a specified step.

        This function iterates over all connected displays, retrieves their current brightness,
        calculates the new brightness by adding the step value, and updates the brightness
        for each display. The brightness is clamped to a maximum of 1.0 (100%).

        :param step: The step size to adjust the brightness. A positive value increases brightness,
                    while a negative value decreases brightness. The step is interpreted as a
                    percentage (e.g., 10 for 10%).
        """
        self.logger.debug(f"Changing brightness by {step}% for all displays...")
        for display in self.connected_displays:
            current_brightness = self.get_brightness(display)
            new_brightness = min(current_brightness + (step / 100), 1.0)
            self.set_brightness(display, new_brightness * 100)
            self.logger.info(f"Brightness changed by {step}% for {display}. New brightness: {new_brightness * 100}%")

    def increase_brightness(self, step=10):
        """
        Increase the brightness of a display.
        :param display: Name of the display (e.g., 'eDP-1')
        :param step: Step size to increase brightness (default: 10%)
        """
        self.logger.debug(f"Increasing brightness by {step}%...")
        self.change_brightness(step)

    def decrease_brightness(self, step=10):
        """
        Decrease the brightness of a display.
        :param display: Name of the display (e.g., 'eDP-1')
        :param step: Step size to decrease brightness (default: 10%)
        """
        self.logger.debug(f"Decreasing brightness by {step}%...")
        self.change_brightness(-step)

    def list_displays(self):
        """
        List all connected displays.
        :return: List of connected display names.
        """
        self.logger.debug("Listing connected displays...")
        return self.connected_displays
    




if __name__ == "__main__":
    dc = DisplayController()
    dc.change_brightness(-50)