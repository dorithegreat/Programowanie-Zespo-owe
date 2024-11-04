from langchain_ollama import OllamaLLM
from openai import OpenAI
from ast import literal_eval

COMMAND_LIST = (
    # "przyciemnić ekran",
    "zmniejszyć jasność",
    "zwiększyć jasność",
    # "podnieść jasność"
    "zmniejszyć głośność",
    # "obniżyć głośność",
    "zwiększyć głośność",
    # "wyłączyć komputer",
    # "zresetować komputer",
)

_PREFIX = (
    f"Sprawdź, czy w poniższym tekście znajduje się jakaś komenda z listy : {', '.join(COMMAND_LIST)}. "
    "lub ich wyrażenia bliskoznaczne. "
    "Jeśli tak, to dodaj ją do listy z Pythona i zwróć w tej formie, np. "
    "['zwiększyć jasność']. Jeśli nie, odpowiedz pustą listą []. Oto tekst: "
)


class CommandsExtractor:
    def __init__(self, model: str):
        self._model = OllamaLLM(model=model)

    def get_commands(self, text: str):
        commands = self._model.invoke(input=_PREFIX + text)
        return literal_eval(commands)


class OpenAICommandsExtractor:
    def __init__(self, model: str):
        self._client = OpenAI()
        self._model_name = model

    def get_commands(self, text: str):
        completion = self._client.chat.completions.create(
            model=self._model_name,
            messages=[{"role": "user", "content": _PREFIX + text}],
        )
        return literal_eval(completion.choices[0].message.content)
