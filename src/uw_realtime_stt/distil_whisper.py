


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
