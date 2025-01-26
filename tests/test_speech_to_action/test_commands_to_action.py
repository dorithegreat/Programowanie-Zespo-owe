import pytest
from unittest.mock import Mock, patch
from src.speech_to_action.commands_to_action import commands_to_action, SpeechCommands as SC


MODULE = "src.speech_to_action.commands_to_action"

@pytest.mark.parametrize(
    "commands, call1, call2", 
    [
        ([SC.BRIGHTNESS_INC.value, f"{SC.OPEN_PROGRAM.value} steam"], SC.BRIGHTNESS_INC, SC.OPEN_PROGRAM),
        ([SC.REBOOT_PC.value, f"{SC.SEARCH_PHRASE.value} słodkie kotki"], SC.REBOOT_PC, SC.SEARCH_PHRASE),
        ([SC.VOLUME_INC.value, SC.BRIGHTNESS_DEC.value], SC.VOLUME_INC, SC.BRIGHTNESS_DEC)
    ]
)

def test_commands_to_action(commands, call1, call2):
    with patch.dict(f"{MODULE}._COMMAND_TO_ACTION_MAPPER", {call1: Mock(), call2: Mock()}) as mock:
        commands_to_action(commands)

        mock[call1].assert_called_once()
        mock[call2].assert_called_once()
