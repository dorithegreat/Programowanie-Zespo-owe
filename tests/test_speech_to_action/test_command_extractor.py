import pytest
from src.speech_to_action.commands_extractor import CommandsExtractor

CASE1 = "Could you increase the brightness and also reset the PC?"
CASE2 = "Please decrease the volume"
CASE3 = "Hey, I want you to turn off the PC"
CASE4 = "Yoo, I love apples so much how about you? Do you like to increase your sugar level?"
CASE5 = "God damn it reset the PC, allright?"

extractor = CommandsExtractor("llama3.2:3b")


@pytest.mark.parametrize(
    "input, expected_output",
    [
        (CASE1, ('increase brightness', 'reset')),
        (CASE2, ('decrease volume')),
        (CASE3, ('turn off')),
        (CASE4, ()),
        (CASE5, ('reset'))
    ])
def test_commands_extractor_on_llama3_2_3b(input, expected_output):
    extracted_commands = extractor.get_commands(input)

    # ęęęęę
    assert expected_output == extracted_commands
