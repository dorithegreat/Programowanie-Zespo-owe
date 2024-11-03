from langchain_ollama import OllamaLLM
from ast import literal_eval

COMMAND_LIST = (
    "przyciemnić ekran",
    "zmniejszyć jasność",

    "zwiększyć jasność",
    "podnieść jasność"

    "zmniejszyć głośność",
    "obniżyć głośność",

    "zwiększyć głośność",

    # "wyłączyć komputer",
    # "zresetować komputer",
)

_PREFIX = (
    f"Sprawdź proszę, czy w poniższym tekście znajdują się komendy z listy : {', '.join(COMMAND_LIST)} lub ich wyrażenia bliskoznaczne. "
    "Jeśli tak, odpowiedz krotką Pythona, która zawiera te komendy, np. ('zwiększyć jasność'). Jeśli nie, odpowiedz pustą krotką (). Oto tekst: "
)


class CommandsExtractor:
    def __init__(self, model: str):
        self._model = OllamaLLM(model=model)

    def get_commands(self, text: str):
        commands = self._model.invoke(input=_PREFIX + text)
        return literal_eval(commands)
