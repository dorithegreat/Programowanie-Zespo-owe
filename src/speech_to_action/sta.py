from speech_to_text import stt
from commands_extractor import OpenAICommandsExtractor
from commands_to_action import commands_to_action


if __name__ == "__main__":
    sttinstance = stt()
    llm = OpenAICommandsExtractor("gpt-4o")
    try:
        while True:
            str = sttinstance.listen(False)
            print(str)
            if str in (" ", "", "\n"):
                continue
            commands_list = llm.get_commands(str)
            print(commands_list)
            commands_to_action(commands_list)
    except KeyboardInterrupt:
        sttinstance.end()
    