from langchain_ollama import OllamaLLM
from openai import OpenAI
from ast import literal_eval
from src.speech_to_action.commands_to_action import SpeechCommands, SpeechArgumentCommands

COMMANDS = [cmd.value for cmd in SpeechCommands]
ARGUMENT_COMMANDS = [cmd.value for cmd in SpeechArgumentCommands]
STANDARD_COMMANDS = list(set(COMMANDS) - set(ARGUMENT_COMMANDS))

_PREFIX = (
    "Przeanalizuj podany tekst i sprawdź, czy zawiera:"
    " 1) Komendy z listy: "
    f"{', '.join(STANDARD_COMMANDS)}, lub ich wyrażenia bliskoznaczne. "
    "    Jeśli znajdziesz takie komendy, zwróć tylko ich listę w formacie: [\"zwiększyć_jasność\", \"otworzyć_plik\"]. "
    f" 2) Prośby by coś {' lub '.join(ARGUMENT_COMMANDS)}, lub ich wyrażenia bliskoznaczne. "
    "    Jeśli znajdziesz takie prośby zwróć tylko ich listę w formacie: [\"otworzyć nazwa_programu\", \"wyszukać fraza\"]. "
    "Jeśli tekst nie zawiera żadnych komend ani próśb, zwróć tylko pustą listę: []. "
    "Oto tekst:"
)


class BaseCommandExtractor:
    def get_commands() -> list[str]:
        """
        ### Returns:
        - a list of commands.

        ### There are two types of commands:
        - Standard commands: Commands that don't have any arguments.
        - Argument commands: Commands that have arguments associated with them.

        ### Example:
        - ['zmniejszyć głośność', 'wyłączyć komputer'] - standard commands
        - ['otworzyć steam'] - argument command
        """


class CommandsExtractor(BaseCommandExtractor):
    def __init__(self, model: str):
        self._model = OllamaLLM(model=model)

    def get_commands(self, text: str) -> list[str]:
        commands = self._model.invoke(input=_PREFIX + text)
        return literal_eval(commands)


class OpenAICommandsExtractor(BaseCommandExtractor):
    def __init__(self, model: str):
        self._client = OpenAI()
        self._model_name = model

    def get_commands(self, text: str) -> list[str]:
        completion = self._client.chat.completions.create(
            model=self._model_name,
            messages=[{"role": "user", "content": _PREFIX + text}],
        )
        return literal_eval(completion.choices[0].message.content)
