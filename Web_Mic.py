import pyaudio
import wave
import openai
import json

# get gpt api key
from API_Key import CHAT_GPT

class Web_Mic_Controler(object):
    def __init__(self):
        self.stop_stream = False
    
    def start(self):
        # 녹음 시작
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 1024
        FILE_NAME = "recording.wav"
        
        audio = pyaudio.PyAudio()
        
        # 오디오 스트림 시작
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)

        frames = []
        
        while not self.stop_stream:
            data = stream.read(CHUNK)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        # wav 파일 저장.
        waveFile = wave.open(FILE_NAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        
    def stop(self):
        # 녹음 종료
        self.stop_stream = True
        
    def speech_to_text(self):
        # 음성 파일의 음성을 문자로 변환
        openai.api_key = CHAT_GPT()

        with open('C:\\Projects\\Chat-Drone\\recording_tset.wav', 'rb') as audio_file:
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file)

        text = json.loads(json.dumps(transcript))["text"]
        return text