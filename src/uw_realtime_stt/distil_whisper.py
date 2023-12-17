import speech_recognition as sr 
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import load_dataset
import io
import numpy as np
import json 
import requests


with open('hf.json', 'r') as file:
    key = json.load(file)


headers = {"Authorization": f"Bearer {key['hf-write']}"}
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v2"


def stt(audio):
    
    # # Convert to WAV bytes
    # audio_bytes = audio.get_wav_data()
    # # Convert to BytesIO object
    # audio_io = io.BytesIO(audio_bytes)
    try:

        response = requests.request("POST", API_URL, headers=headers, data=audio)
        transcription = json.loads(response.content.decode("utf-8"))
        return transcription
        
    except sr.UnknownValueError:
        # If the audio wasn't understood, it's okay to just keep listening
        print("stt")
        pass
    except sr.RequestError:
        print("API unavailable. Please check your internet connection")
        return False
