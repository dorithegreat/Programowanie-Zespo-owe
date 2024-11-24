from enum import Enum

class SpeechCommands(Enum):
    BRIGHTNESS_INC = "zwiększyć_jasność"
    BRIGHTNESS_DEC = "zmniejszyć_jasność"
    VOLUME_INC = "zwiększyć_głośność"
    VOLUME_DEC = "zmniejszyć_głośność"
    SHUTDOWN_PC = "wyłączyć_komputer"
    REBOOT_PC = "zresetować_komputer"
    OPEN_PROGRAM = "otworzyć"
    SEARCH_PHRASE = "wyszukać"


class SpeechArgumentCommands(Enum):
    OPEN_PROGRAM = SpeechCommands.OPEN_PROGRAM.value
    SEARCH_PHRASE = SpeechCommands.SEARCH_PHRASE.value
