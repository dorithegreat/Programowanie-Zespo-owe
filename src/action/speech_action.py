import subprocess
import alsaaudio


def handle_errors(action):
    def wrapper():
        try:
            action()
        except:
            pass
    return wrapper


def increase_brightness():
    pass


def decrease_brightness():
    pass


def increase_volume():
    _change_volume(15)
    

def decrease_volume():
    _change_volume(-15)


@handle_errors
def _change_volume(value):
    mixer = alsaaudio.Mixer()
    current_volume = mixer.getvolume()
    mixer.setvolume(current_volume[1] + value)


def shutdown_pc():
    pass


def reboot_pc():
    pass


def open_program(name: str):
    pass



def close_program(name: str):
    subprocess.run(["pkill", name])



def search_phrase(phrase: str):
    subprocess.run(["xdg-open", "https://search.brave.com/search?q=" + phrase])
