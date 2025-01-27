import subprocess
from src.computer_controller.browser_controller import BrowserController
from src.computer_controller.display_controller import DisplayController
from src.computer_controller.volume_controller import VolumeController
from src.computer_controller.utils import open_program as op, shut_program, shutdown_computer, reboot_computer

browser_controller = BrowserController()
display_controller = DisplayController()
volume_controller = VolumeController()


def increase_brightness():
    display_controller.increase_brightness()


def decrease_brightness():
    display_controller.decrease_brightness()


def _change_brightness(value: int):
    display_controller.change_brightness(value)

def increase_volume():
    volume_controller.increase_volume()
    

def decrease_volume():
    volume_controller.decrease_volume()


def _change_volume(value):
    volume_controller.decrease_volume(value)

def shutdown_pc():
    shutdown_computer()


def reboot_pc():
    reboot_computer()


def open_program(name: str):
    op(name)



def close_program(name: str):
    shut_program(name)


def search_phrase(phrase: str):
    browser_controller.search(phrase)
