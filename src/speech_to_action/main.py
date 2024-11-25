from src.speech_to_action.speech_to_text import stt
from src.speech_to_action.commands_extractor import OpenAICommandsExtractor
from src.speech_to_action.commands_to_action import commands_to_action


if __name__=="__main__":
    sttinstance = stt()
    llm = OpenAICommandsExtractor("")
    try:
        while True:
            str = sttinstance.listen()
            clist = llm.get_commands(str)
            commands_to_action(clist)
            print(clist)
    except KeyboardInterrupt:
        sttinstance.end()
    
