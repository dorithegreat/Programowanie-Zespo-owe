from typing import Callable
from src.speech_to_action.common import SpeechCommands as SC

from src.action.speech_action import (
    decrease_brightness, increase_brightness, decrease_volume, increase_volume,
    shutdown_pc, reboot_pc, open_program, search_phrase
)

_COMMAND_TO_ACTION_MAPPER: dict[str, Callable] = {
    SC.BRIGHTNESS_DEC: decrease_brightness,
    SC.BRIGHTNESS_INC: increase_brightness,
    SC.VOLUME_DEC: decrease_volume,
    SC.VOLUME_INC: increase_volume,
    SC.SHUTDOWN_PC: shutdown_pc,
    SC.REBOOT_PC: reboot_pc,
    SC.OPEN_PROGRAM: open_program,
    SC.SEARCH_PHRASE: search_phrase,
}

def commands_to_action(commands: list):
    for command in commands:
        if command.count(" ") >= 1:
            cmd = SC(command.split(" ")[0])
            arg = " ".join(command.split(" ")[1:])
            _COMMAND_TO_ACTION_MAPPER[cmd](arg)
        else:
            _COMMAND_TO_ACTION_MAPPER[SC(command)]()
