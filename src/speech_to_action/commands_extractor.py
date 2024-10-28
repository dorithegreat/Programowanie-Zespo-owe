from langchain_ollama import OllamaLLM
from ast import literal_eval

COMMAND_LIST = (
    "increase volume",
    "decrease volume",
    "increase brightness",
    "decrease brightness",
    "turn off",
    "reset",
)

PREFIX = (
    "Below I will send you a request from a person. I want you to "
    "detect if the person is asking to do something from the following "
    f"command list: {', '.join(COMMAND_LIST)}. If you detect a command return a "
    "pythonic tuple, e.g. if the person asks to decrease brightness then reply to "
    "me ONLY with ('decrese brightness'). If you did not detect any command then "
    "reply to me ONLY with (). Here is the text on which you should act: "
)


class CommandsExtractor:
    __slots__ = "_model"

    def __init__(self, model: str):
        self._model = OllamaLLM(model=model)

    def get_commands(self, text: str):
        commands = self._model.invoke(input=PREFIX + text)
        return literal_eval(commands)
