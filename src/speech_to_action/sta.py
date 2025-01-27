from src.speech_to_action.speech_to_text import stt
from src.speech_to_action.commands_extractor import OpenAICommandsExtractor
from src.speech_to_action.commands_to_action import commands_to_action


if __name__ == "__main__":
    sttinstance = stt()
    llm = OpenAICommandsExtractor("gpt-4o")
    str = ""
    try:
        while True:
            str = sttinstance.listen(False)
            print(str)
            if str in (" ", "", "\n"):
                continue
            if "hej asystencie" in str:
                print("-")
                str = sttinstance.listen(False)
                commands_list = llm.get_commands(str)
                commands_to_action(commands_list)
    except KeyboardInterrupt:
        sttinstance.end()
    