import pytest
from src.speech_to_action.commands_extractor import OpenAICommandsExtractor

PATTERN1 = "Lorem ipsum. Czy możesz {}? Lorem ipsum."
PATTERN2 = "Lorem ipsum. Proszę, {}. Lorem ipsum."
PATTERN3 = "Lorem ipsum. Hej, chcę żebyś {}. Lorem ipsum."
PATTERN4 = "Lorem ipsum, {}? Lorem ipsum."

DECREASING_BRIGHTNESS_CASE1 = PATTERN1.format("zmniejszyć jasność")
DECREASING_BRIGHTNESS_CASE2 = PATTERN2.format("zmniejsz jasność")
DECREASING_BRIGHTNESS_CASE3 = PATTERN3.format("zmniejszył jasność")
DECREASING_BRIGHTNESS_CASE4 = PATTERN4.format("zmniejszyłbyś jasność")
DECREASING_BRIGHTNESS_CASE5 = PATTERN1.format("przyciemnić ekran")
DECREASING_BRIGHTNESS_CASE6 = PATTERN2.format("przyciemnij ekran")
DECREASING_BRIGHTNESS_CASE7 = PATTERN3.format("przyciemnił ekran")
DECREASING_BRIGHTNESS_CASE8 = PATTERN4.format("przyciemniłbyś ekran")
DECREASING_BRIGHTNESS_CASE9 = PATTERN1.format("ściemnić ekran")
DECREASING_BRIGHTNESS_CASE10 = PATTERN2.format("ściemnij ekran")
DECREASING_BRIGHTNESS_CASE11 = PATTERN3.format("ściemnił ekran")
DECREASING_BRIGHTNESS_CASE12 = PATTERN4.format("ściemniłbyś ekran")
# DECREASING_BRIGHTNESS_CASE13 = "Wow, uwielbiam jabłka, a ty? Lubisz zmniejszać swój poziom cukru?"

INCREASING_BRIGHTNESS_CASE1 = PATTERN1.format("zwiększyć jasność")
INCREASING_BRIGHTNESS_CASE2 = PATTERN2.format("zwiększ jasność")
INCREASING_BRIGHTNESS_CASE3 = PATTERN3.format("zwiększył jasność")
INCREASING_BRIGHTNESS_CASE4 = PATTERN4.format("zwiększyłbyś jasność")
INCREASING_BRIGHTNESS_CASE5 = PATTERN1.format("podnieść jasność")
INCREASING_BRIGHTNESS_CASE6 = PATTERN2.format("podnieś jasność")
INCREASING_BRIGHTNESS_CASE7 = PATTERN3.format("podniósł jasność")
INCREASING_BRIGHTNESS_CASE8 = PATTERN4.format("podniósłbyś jasność")


DECREASING_VOLUME_CASE1 = PATTERN1.format("ściszyć głośność")
DECREASING_VOLUME_CASE2 = PATTERN2.format("ścisz głośność")
DECREASING_VOLUME_CASE3 = PATTERN3.format("ściszył głośność")
DECREASING_VOLUME_CASE4 = PATTERN4.format("ściszyłbyś głośność")
DECREASING_VOLUME_CASE5 = PATTERN1.format("przyciszyć głośność")
DECREASING_VOLUME_CASE6 = PATTERN2.format("przycisz głośność")
DECREASING_VOLUME_CASE7 = PATTERN3.format("przyciszył głośność")
DECREASING_VOLUME_CASE8 = PATTERN4.format("przyciszyłbyś głośność")
DECREASING_VOLUME_CASE9 = PATTERN1.format("obniżyć głośność")
DECREASING_VOLUME_CASE10 = PATTERN2.format("obniż głośność")
DECREASING_VOLUME_CASE11 = PATTERN3.format("obniżył głośność")
DECREASING_VOLUME_CASE12 = PATTERN4.format("obniżyłbyś głośność")
DECREASING_VOLUME_CASE13 = PATTERN1.format("zmniejszyć głośność")
DECREASING_VOLUME_CASE14 = PATTERN2.format("zmniejsz głośność")
DECREASING_VOLUME_CASE15 = PATTERN3.format("zmniejszył głośność")
DECREASING_VOLUME_CASE16 = PATTERN4.format("zmniejszyłbyś głośność")

INCREASING_VOLUME_CASE1 = PATTERN1.format("zwiększyć głośność")
INCREASING_VOLUME_CASE2 = PATTERN2.format("zwiększ głośność")
INCREASING_VOLUME_CASE3 = PATTERN3.format("zwiększył głośność")
INCREASING_VOLUME_CASE4 = PATTERN4.format("zwiększyłbyś głośność")

extractor = OpenAICommandsExtractor("gpt-4o")


@pytest.mark.parametrize(
    "input, expected_output",
    [
        (DECREASING_BRIGHTNESS_CASE1, "zmniejszyć jasność"),
        (DECREASING_BRIGHTNESS_CASE2, "zmniejszyć jasność"),
        (DECREASING_BRIGHTNESS_CASE3, "zmniejszyć jasność"),
        (DECREASING_BRIGHTNESS_CASE4, "zmniejszyć jasność"),
        (DECREASING_BRIGHTNESS_CASE5, "przyciemnić ekran"),
        (DECREASING_BRIGHTNESS_CASE6, "przyciemnić ekran"),
        (DECREASING_BRIGHTNESS_CASE7, "przyciemnić ekran"),
        (DECREASING_BRIGHTNESS_CASE8, "przyciemnić ekran"),
        (DECREASING_BRIGHTNESS_CASE9, ("ściemnić ekran")),
        (DECREASING_BRIGHTNESS_CASE10, ("ściemnić ekran")),
        (DECREASING_BRIGHTNESS_CASE11, ("ściemnić ekran")),
        (DECREASING_BRIGHTNESS_CASE12, ("ściemnić ekran")),
        # (DECREASING_BRIGHTNESS_CASE13, "")
    ],
)
def test_commands_extractor_on_decreasing_brightness(input, expected_output):
    extracted_commands = extractor.get_commands(input)

    assert "zmniejszyć jasność" == " ".join(extracted_commands)


@pytest.mark.parametrize(
    "input, expected_output",
    [
        (INCREASING_BRIGHTNESS_CASE1, "zwiększyć jasność"),
        (INCREASING_BRIGHTNESS_CASE2, "zwiększyć jasność"),
        (INCREASING_BRIGHTNESS_CASE3, "zwiększyć jasność"),
        (INCREASING_BRIGHTNESS_CASE4, "zwiększyć jasność"),
        (INCREASING_BRIGHTNESS_CASE5, "podnieść jasność"),
        (INCREASING_BRIGHTNESS_CASE6, "podnieść jasność"),
        (INCREASING_BRIGHTNESS_CASE7, "podnieść jasność"),
        (INCREASING_BRIGHTNESS_CASE8, "podnieść jasność"),
    ],
)
def test_commands_extractor_on_increasing_brightness(input, expected_output):
    extracted_commands = extractor.get_commands(input)

    assert "zwiększyć jasność" == " ".join(extracted_commands)


@pytest.mark.parametrize(
    "input, expected_output",
    [
        (DECREASING_VOLUME_CASE1, "ściszyć głośność"),
        (DECREASING_VOLUME_CASE2, "ściszyć głośność"),
        (DECREASING_VOLUME_CASE3, "ściszyć głośność"),
        (DECREASING_VOLUME_CASE4, "ściszyć głośność"),
        (DECREASING_VOLUME_CASE5, "przyciszyć głośność"),
        (DECREASING_VOLUME_CASE6, "przyciszyć głośność"),
        (DECREASING_VOLUME_CASE7, "przyciszyć głośność"),
        (DECREASING_VOLUME_CASE8, "przyciszyć głośność"),
        (DECREASING_VOLUME_CASE9, "obniżyć głośność"),
        (DECREASING_VOLUME_CASE10, "obniżyć głośność"),
        (DECREASING_VOLUME_CASE11, "obniżyć głośność"),
        (DECREASING_VOLUME_CASE12, "obniżyć głośność"),
        (DECREASING_VOLUME_CASE13, "zmniejszyć głośność"),
        (DECREASING_VOLUME_CASE14, "zmniejszyć głośność"),
        (DECREASING_VOLUME_CASE15, "zmniejszyć głośność"),
        (DECREASING_VOLUME_CASE16, "zmniejszyć głośność"),
    ],
)
def test_commands_extractor_on_decreasing_volume(input, expected_output):
    extracted_commands = extractor.get_commands(input)

    assert "zmniejszyć głośność" == " ".join(extracted_commands)


@pytest.mark.parametrize(
    "input",
    [
        INCREASING_VOLUME_CASE1,
        INCREASING_VOLUME_CASE2,
        INCREASING_VOLUME_CASE3,
        INCREASING_VOLUME_CASE4,
    ],
)
def test_commands_extractor_on_increasing_volume(input):
    extracted_commands = extractor.get_commands(input)

    assert "zwiększyć głośność" == " ".join(extracted_commands)
