import whisper
import pyaudio
import math
import struct
import wave
import time
import os


class stt:
    SHORT_NORMALIZE = (1.0/32768.0)
    CHUNKSIZE = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    swidth = 2

    TIMEOUT_LENGTH = 2

    arbitrary_names_to_prog_names = {}
    prompt_prog_name = ""


    def getProgNames(self):
        progNames = set()
        folderlist = os.getenv('PATH').split(':')
        for i in folderlist:
            for j in os.listdir(i):
                if os.access(i+"/"+j,os.X_OK):
                    progNames.add(j.replace("-","").replace(".",""))
                    self.arbitrary_names_to_prog_names[j.replace("-","").replace(".","")] = j
        res = "Glossary: "
        for i in progNames:
            res += i
            res += ", "
        self.prompt_prog_name = res[:-2]
        return

    def __init__(self) -> None:
        self.model = whisper.load_model("./model/whisper-finetuned-epoch.pt")
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                channels=1,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNKSIZE)
        self.getProgNames()
        self.Threshold = 0.8
        self.background_noise_level(5)
        print("Ready")

    def rms(self,frame):
        count = len(frame) / self.swidth
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * self.SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000
    
    def background_noise_level(self,duration):
        frames = []
        current = time.time()
        end  = time.time() + duration
        while current <= end:
            data = self.stream.read(self.CHUNKSIZE)
            frames.append(self.rms(data))
            current = time.time()
        self.Threshold = 3.0 + sum(frames) / len(frames)
        print(self.Threshold)

    def startrecord(self,file_path,firstframe):
        frames = [firstframe]
        current = time.time()
        end  =time.time() + self.TIMEOUT_LENGTH

        while current <= end:
            data = self.stream.read(self.CHUNKSIZE)

            if self.rms(data) >= self.Threshold:
                end = time.time() + self.TIMEOUT_LENGTH
            current = time.time()
            frames.append(data)

        wf = wave.open(file_path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(frames))
        wf.close

    def start(self,file_path):
        while True:
            input = self.stream.read(self.CHUNKSIZE)
            rms_val = self.rms(input)
            if rms_val > self.Threshold:
                print("started")
                self.startrecord(file_path,input)
                break

    def end(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        
    def listen(self,use_prog_names: bool):
        temp_file = "temp.wav"
        self.start(temp_file)
        if use_prog_names:
            result = self.model.transcribe(temp_file,language="pl",initial_prompt = self.prompt_prog_name)
        else:
            result = self.model.transcribe(temp_file,language="pl")
        os.remove(temp_file)
        return result['text']+"\n"
