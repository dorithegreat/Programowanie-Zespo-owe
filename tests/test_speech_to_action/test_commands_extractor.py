import pytest
from src.speech_to_action.commands_to_action import SpeechCommands as SC
from src.speech_to_action.commands_extractor import OpenAICommandsExtractor

PATTERN1 = "Lorem ipsum. Czy możesz {}? Lorem ipsum."
PATTERN2 = "Lorem ipsum. Proszę, {}. Lorem ipsum."
PATTERN3 = "Lorem ipsum. Hej, chcę żebyś {}. Lorem ipsum."
PATTERN4 = "Lorem ipsum, {}? Lorem ipsum."

PATTERNS = (PATTERN1, PATTERN2, PATTERN3, PATTERN4)


CASES = {
    "zmniejszyć_jasność": [
        ("zmniejszyć jasność", "zmniejsz jasność", "zmniejszył jasność", "zmniejszyłbyś jasność"),
        ("przyciemnić ekran", "przyciemnij ekran", "przyciemnił ekran", "przyciemniłbyś ekran"),
        ("ściemnić ekran", "ściemnij ekran", "ściemnił ekran", "ściemniłbyś ekran")
    ],
    "zwiększyć_jasność": [
        ("zwiększyć jasność", "zwiększ jasność", "zwiększył jasność", "zwiększyłbyś jasność"),
        ("podnieść jasność", "podnieś jasność", "podniósł jasność", "podniósłbyś jasność")
    ],
    "zmniejszyć_głośność": [
        ("ściszyć głośność", "ścisz głośność", "ściszył głośność", "ściszyłbyś głośność"),
        ("ściszyć dźwięk", "ścisz dźwięk", "ściszył dźwięk", "ściszyłbyś dźwięk"),
        ("przyciszyć głośność", "przycisz głośność", "przyciszył głośność", "przyciszyłbyś głośność"),
        ("przyciszyć dźwięk", "przycisz dźwięk", "przyciszył dźwięk", "przyciszyłbyś dźwięk"),
        ("obniżyć głośność", "obniż głośność", "obniżył głośność", "obniżyłbyś głośność"),
        ("obniżyć dźwięk", "obniż dźwięk", "obniżył dźwięk", "obniżyłbyś dźwięk"),
        ("zmniejszyć głośność", "zmniejsz głośność", "zmniejszył głośność", "zmniejszyłbyś głośność"),
        ("zmniejszyć dźwięk", "zmniejsz dźwięk", "zmniejszył dźwięk", "zmniejszyłbyś dźwięk"),
    ],
    "zwiększyć_głośność": [
        ("zwiększyć głośność", "zwiększ głośność", "zwiększył głośność", "zwiększyłbyś głośność"),
        ("zwiększyć dźwięk", "zwiększ dźwięk", "zwiększył dźwięk", "zwiększyłbyś dźwięk"),
        ("podnieść głośność", "podnieś głośność", "podniósł głośność", "podniósłbyś głośność"),
        ("podnieść dźwięk", "podnieś dźwięk", "podniósł dźwięk", "podniósłbyś dźwięk"),
    ],
    "wyłączyć_komputer": [
        ("wyłączyć komputer", "wyłącz komputer", "wyłączył komputer", "wyłączyłbyś komputer")
    ],
    "zresetować_komputer": [
        ("zresetować komputer", "zresetuj komputer", "zresetował komputer", "zresetowałbyś komputer"), 
        ("uruchomić ponownie komputer", "uruchom ponownie komputer", "uruchomił ponownie komputer", "uruchomiłbyś ponownie komputer")
    ],
}

CASES_WITH_ARGUMENTS = {
    "otworzyć": [
        ("otworzyć firefox", "otwórz steam", "otworzył libreoffice", "otworzyłbyś visual studio code"),
        ("uruchomić firefox", "uruchom steam", "uruchomił libreoffice", "uruchomiłbyś visual studio code"),
    
    ],
    "zamknąć": [
        ("zamknąć firefox", "zamknij steam", "zamknął libreoffice", "zamknąłbyś visual studio code"),
    ],
    "wyszukać": [
        ("wyszukać czy śliwki są zielone", "wyszukaj Polska", "wyszukał najmniejszą liczbę pierwszą", "wyszukałbyś pogodę w Lesznie"),
    ]
}

DIFFERENT_CASES = {
    "tricky": [
        "Wow, uwielbiam jabłka, a ty? Lubisz zmniejszać swój poziom cukru?",
        "Drogi kolego prosze zwiększ poziom tej gry.",
        "Jarek, weź ścisz telefon.",
        "Podnieś ten kapelusz z ziemi",
        "Wyłącz światło",
        "Zresetuj swój umysł"
    ],
    "multiple": [
        ("Czy mógłbyś podnieść jasność oraz uruchomić ponownie komputer?", ("zwiększyć_jasność", "zresetować_komputer")),
        ("Czy możesz zwiększyć głośność i wyłączyć komputer?", ("zwiększyć_głośność", "wyłączyć_komputer")),
        ("Otwórz paint oraz podłośnij dźwięk", ("otworzyć paint", "zwiększyć_głośność")),
        ("Wyszukaj gdzie raki zimują i wyłącz komputer", ("wyszukać gdzie raki zimują", "wyłączyć_komputer"))
    ]
}


def get_cases(type: SC) -> list[str]:
    cases = CASES[type.value]

    return [
        PATTERNS[k].format(j) for i in cases for k, j in enumerate(i)
    ]


def get_cases_with_arguments(type: SC):
    cases = CASES_WITH_ARGUMENTS[type.value]

    return [
        (PATTERNS[k].format(j), [type.value + " " + " ".join(j.split(" ")[1:])]) 
        for i in cases for k, j in enumerate(i)
    ]


extractor = OpenAICommandsExtractor("gpt-4o")


@pytest.mark.parametrize(
    "input",
    get_cases(SC.BRIGHTNESS_INC),
)
def test_commands_extractor_on_decreasing_brightness(input):
    extracted_commands = extractor.get_commands(input)

    assert SC.BRIGHTNESS_INC.value == " ".join(extracted_commands)


@pytest.mark.parametrize(
    "input",
    get_cases(SC.BRIGHTNESS_DEC),
)
def test_commands_extractor_on_increasing_brightness(input):
    extracted_commands = extractor.get_commands(input)

    assert SC.BRIGHTNESS_DEC.value == " ".join(extracted_commands)


@pytest.mark.parametrize(
    "input",
    get_cases(SC.VOLUME_DEC),
)
def test_commands_extractor_on_decreasing_volume(input):
    extracted_commands = extractor.get_commands(input)

    assert SC.VOLUME_DEC.value == " ".join(extracted_commands)


@pytest.mark.parametrize(
    "input",
    get_cases(SC.VOLUME_INC),
)
def test_commands_extractor_on_increasing_volume(input):
    extracted_commands = extractor.get_commands(input)

    assert SC.VOLUME_INC.value == " ".join(extracted_commands)


@pytest.mark.parametrize(
    "input",
    get_cases(SC.SHUTDOWN_PC),
)
def test_commands_extractor_on_turning_off_pc(input):
    extracted_commands = extractor.get_commands(input)

    assert SC.SHUTDOWN_PC.value == " ".join(extracted_commands)


@pytest.mark.parametrize(
    "input",
    get_cases(SC.REBOOT_PC),
)
def test_commands_extractor_on_resetting_pc(input):
    extracted_commands = extractor.get_commands(input)

    assert SC.REBOOT_PC.value == " ".join(extracted_commands)


@pytest.mark.parametrize(
    "input",
    DIFFERENT_CASES["tricky"],
)
def test_commands_extractor_on_tricky_questions(input):
    extracted_commands = extractor.get_commands(input)

    assert [] == extracted_commands


@pytest.mark.parametrize(
    "input, expected_output",
    DIFFERENT_CASES["multiple"],
)
def test_commands_extractor_on_multiple_questions(input, expected_output):
    extracted_commands = extractor.get_commands(input)

    assert set(expected_output) == set(tuple((extracted_commands)))


@pytest.mark.parametrize(
    "input, expected_output",
    get_cases_with_arguments(SC.OPEN_PROGRAM)
)
def test_commands_extractor_on_opening_program(input, expected_output):
    extracted_commands = extractor.get_commands(input)

    assert expected_output == extracted_commands


@pytest.mark.parametrize(
    "input, expected_output",
    get_cases_with_arguments(SC.CLOSE_PROGRAM)
)
def test_commands_extractor_on_closing_program(input, expected_output):
    extracted_commands = extractor.get_commands(input)

    assert expected_output == extracted_commands


@pytest.mark.parametrize(
    "input, expected_output",
    get_cases_with_arguments(SC.SEARCH_PHRASE),
)
def test_commands_extractor_on_searching(input, expected_output):
    extracted_commands = extractor.get_commands(input)

    assert expected_output == extracted_commands
