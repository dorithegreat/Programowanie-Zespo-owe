from typing import Callable
from enum import Enum
from src.action.speech_action import (
    decrease_brightness, increase_brightness, decrease_volume, increase_volume,
    shutdown_pc, reboot_pc, open_program, search_phrase, close_program
)


class SpeechCommands(Enum):
    BRIGHTNESS_INC = "zwiększyć_jasność"
    BRIGHTNESS_DEC = "zmniejszyć_jasność"
    VOLUME_INC = "zwiększyć_głośność"
    VOLUME_DEC = "zmniejszyć_głośność"
    SHUTDOWN_PC = "wyłączyć_komputer"
    REBOOT_PC = "zresetować_komputer"
    OPEN_PROGRAM = "otworzyć"
    CLOSE_PROGRAM = "zamknąć"
    SEARCH_PHRASE = "wyszukać"


class SpeechArgumentCommands(Enum):
    OPEN_PROGRAM = SpeechCommands.OPEN_PROGRAM.value
    CLOSE_PROGRAM = SpeechCommands.CLOSE_PROGRAM.value
    SEARCH_PHRASE = SpeechCommands.SEARCH_PHRASE.value


_COMMAND_TO_ACTION_MAPPER: dict[str, Callable] = {
    SpeechCommands.BRIGHTNESS_DEC: decrease_brightness,
    SpeechCommands.BRIGHTNESS_INC: increase_brightness,
    SpeechCommands.VOLUME_DEC: decrease_volume,
    SpeechCommands.VOLUME_INC: increase_volume,
    SpeechCommands.SHUTDOWN_PC: shutdown_pc,
    SpeechCommands.REBOOT_PC: reboot_pc,
    SpeechCommands.OPEN_PROGRAM: open_program,
    SpeechCommands.CLOSE_PROGRAM: close_program,
    SpeechCommands.SEARCH_PHRASE: search_phrase,
}

def commands_to_action(commands: list):
    for command in commands:
        if command.count(" ") >= 1:
            cmd = SpeechCommands(command.split(" ")[0])
            arg = " ".join(command.split(" ")[1:])
            _COMMAND_TO_ACTION_MAPPER[cmd](arg)
        else:
            _COMMAND_TO_ACTION_MAPPER[SpeechCommands(command)]()
