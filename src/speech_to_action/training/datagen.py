import pyaudio
import math
import struct
import wave
import time
import os
from pydub import AudioSegment

voice_dir = "test2/"

class stt:
    SHORT_NORMALIZE = (1.0/32768.0)
    CHUNKSIZE = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    swidth = 2

    TIMEOUT_LENGTH = 2

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
        self.Threshold = 2.0 + sum(frames) / len(frames)
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

        sound = AudioSegment.from_wav(file_path)
        sound.export(file_path+".mp3", format='mp3')

        os.remove(file_path)

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

def genfile(i):
    res = "0000" + str(i)
    res = res[len(res) - 4:]
    return voice_dir+res+"test"
def main2():
    i = 1 + len(os.listdir(voice_dir))
    print(i)
    sttinstance = stt()
    print("Started")
    sttinstance.background_noise_level(5)
    time.sleep(2)
    try:
        while True:
            s = genfile(i)
            temp_file = s
            sttinstance.start(temp_file)
            text = input("Wpisz tekst: ")
            f = open(voice_dir+"metadata.csv","a")
            f.write(s.split("/")[1]+".mp3,"+text+"\n")
            f.close()
            print(s)
            i += 1
    except KeyboardInterrupt:
        print("Stop")
    finally:
        sttinstance.end()

main2()