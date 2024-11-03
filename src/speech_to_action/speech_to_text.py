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

    TIMEOUT_LENGTH = 1

    def __init__(self) -> None:
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                channels=1,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNKSIZE)
        self.Threshold = 0.8

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
        print("Measure voice level for")
        print("Started recording")
        frames = []
        current = time.time()
        end  = time.time() + duration
        while current <= end:
            data = self.stream.read(self.CHUNKSIZE)
            frames.append(self.rms(data))
            current = time.time()
        self.Threshold = 0.7 + sum(frames) / len(frames)
        print(self.Threshold)

    def startrecord(self,file_path,firstframe):
        print("Started recording")
        frames = [firstframe]
        current = time.time()
        end  =time.time() + self.TIMEOUT_LENGTH

        while current <= end:
            data = self.stream.read(self.CHUNKSIZE)

            if self.rms(data) >= self.Threshold:
                end = time.time() + self.TIMEOUT_LENGTH
            current = time.time()
            frames.append(data)

        print("Writting to file")

        wf = wave.open(file_path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(frames))
        wf.close

    def start(self,file_path):
        print("Listening")
        while True:
            input = self.stream.read(self.CHUNKSIZE)
            rms_val = self.rms(input)
            if rms_val > self.Threshold:
                self.startrecord(file_path,input)
                break
    def end(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()






# p = pyaudio.PyAudio()
# stream = p.open(format=pyaudio.paInt16,
#                 channels=1,
#                 rate=RATE,
#                 input=True,
#                 frames_per_buffer=CHUNKSIZE)

trans = ""
sttinstance = stt()
model = whisper.load_model("small")
print("Started")
sttinstance.background_noise_level(5)
time.sleep(2)
try:
    while True:
        temp_file = "temp.wav"
        sttinstance.start(temp_file)
        result = model.transcribe(temp_file,language="pl")
        print(result['text']+"\n")
        trans += result['text'] + " "
        os.remove(temp_file)
except KeyboardInterrupt:
    print("Stop")
finally:
    print("LOG: "+trans)
    sttinstance.end()

