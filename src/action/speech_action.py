import subprocess
import screen_brightness_control as sbc
import alsaaudio
import os


BRIGHTNESS_CHANGE = 15
VOLUME_CHANGE = 15


def handle_errors(action):
    def wrapper(arg):
        try:
            action(arg)
        except:
            pass
    return wrapper


def increase_brightness():
    _change_brightness(BRIGHTNESS_CHANGE)


def decrease_brightness():
    _change_brightness(-BRIGHTNESS_CHANGE)


@handle_errors
def _change_brightness(value: int):
    """Works only on X11"""
    for monitor in sbc.list_monitors():
        current_brightness = sbc.get_brightness(display=monitor)
        sbc.set_brightness(current_brightness[0] + value)
        
        
def increase_volume():
    _change_volume(VOLUME_CHANGE)
    

def decrease_volume():
    _change_volume(-VOLUME_CHANGE)


@handle_errors
def _change_volume(value):
    mixer = alsaaudio.Mixer()
    current_volume = mixer.getvolume()
    mixer.setvolume(current_volume[1] + value)


def shutdown_pc():
    os.system("sudo shutdown now")


def reboot_pc():
    os.system("sudo reboot now")


def open_program(name: str):
    name = name.split(" ")
    try:
        p = subprocess.Popen(name)
    except Exception:
        return
    return


@handle_errors
def close_program(name: str):
    subprocess.run(["pkill","-f", name])


@handle_errors
def search_phrase(phrase: str):
    subprocess.run(["xdg-open", "https://search.brave.com/search?q=" + phrase])
