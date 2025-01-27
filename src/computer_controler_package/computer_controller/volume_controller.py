import subprocess as sp
from computer_controller.log import get_logger  # Replace 'your_logger_module' with the actual module name


class VolumeController:
    _instance = None  # Singleton instance

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance of VolumeController is created."""
        if cls._instance is None:
            cls._instance = super(VolumeController, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the Singleton instance."""
        if self._initialized:
            return
        self._initialized = True
        self.logger = get_logger("VolumeController")  # Initialize logger
        self.logger.debug("Initializing VolumeController...")

    def set_volume(self, volume_percent):
        """
        Set the volume to a specific percentage using ALSA.
        :param volume_percent: Volume level (0% to 100%)
        """
        # Ensure the volume is within valid range (0% to 100%)
        volume_percent = max(0, min(volume_percent, 100))
        self.logger.debug(f"Setting volume to {volume_percent}%")
        sp.run(['amixer', 'set', 'Master', f'{volume_percent}%'])
        self.logger.info(f"Volume set to {volume_percent}%")

    def increase_volume(self, step=5):
        """
        Increase the volume by a specified step.
        :param step: Step size to increase volume (default: 5%)
        """
        self.logger.debug(f"Increasing volume by {step}%")
        sp.run(['amixer', 'set', 'Master', f'{step}%+'])
        self.logger.info(f"Volume increased by {step}%")

    def decrease_volume(self, step=5):
        """
        Decrease the volume by a specified step.
        :param step: Step size to decrease volume (default: 5%)
        """
        self.logger.debug(f"Decreasing volume by {step}%")
        sp.run(['amixer', 'set', 'Master', f'{step}%-'])
        self.logger.info(f"Volume decreased by {step}%")

    def mute(self):
        """Mute the sound."""
        self.logger.debug("Muting sound...")
        sp.run(['amixer', 'set', 'Master', 'mute'])
        sp.run(['amixer', 'set', 'Speaker', 'mute'])
        sp.run(['amixer', 'set', 'Headphone', 'mute'])
        self.logger.info("Sound muted")

    def unmute(self):
        """Unmute the sound."""
        self.logger.debug("Unmuting sound...")
        sp.run(['amixer', 'set', 'Master', 'unmute'])
        sp.run(['amixer', 'set', 'Speaker', 'unmute'])
        sp.run(['amixer', 'set', 'Headphone', 'unmute'])
        self.logger.info("Sound unmuted")

    def toggle_mute(self):
        """Toggle mute state."""
        self.logger.debug("Toggling mute state...")
        result = sp.run(['amixer', 'get', 'Master'], capture_output=True, text=True)
        if '[off]' in result.stdout:  # If muted, unmute
            self.unmute()
        else:  # If unmuted, mute
            self.mute()
        self.logger.info("Mute state toggled")




if __name__ == "__main__":
    from time import sleep
    vc = VolumeController()
    for i in range(10):
        vc.decrease_volume(5)
        sleep(1)

    for i in range(10):
        vc.increase_volume(5)
        sleep(1)

    vc.toggle_mute()
    sleep(3)
    vc.toggle_mute()
    sleep(3)
