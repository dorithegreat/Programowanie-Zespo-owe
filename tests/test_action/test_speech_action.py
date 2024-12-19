from src.action.speech_action import (
    BRIGHTNESS_CHANGE, VOLUME_CHANGE, increase_brightness, decrease_brightness,
    increase_volume, decrease_volume
)
import screen_brightness_control as sbc
import alsaaudio


def test_changing_brightness():
    start_brightness = [sbc.get_brightness(display=monitor) for monitor in sbc.list_monitors()]
    expected_brightness_after_increase = [x + BRIGHTNESS_CHANGE for x in start_brightness]
    
    increase_brightness()
    brightness_after_increase = [sbc.get_brightness(display=monitor) for monitor in sbc.list_monitors()]

    assert expected_brightness_after_increase == brightness_after_increase
    
    decrease_brightness()
    brightness_after_decrease = [sbc.get_brightness(display=monitor) for monitor in sbc.list_monitors()]

    assert start_brightness == brightness_after_decrease


def test_changing_volume():
    mixer = alsaaudio.Mixer()
    start_volume = mixer.getvolume()[1]
    expected_volume_after_increase = start_volume + VOLUME_CHANGE

    increase_volume()
    volume_after_increase = mixer.getvolume()[1]

    assert expected_volume_after_increase == volume_after_increase

    decrease_volume()
    volume_after_decrease = mixer.getvolume()[1]

    assert start_volume == volume_after_decrease

