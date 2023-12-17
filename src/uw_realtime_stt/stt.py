# ============================================================================
# STT.py
# 
# ============================================================================

import speech_recognition as sr 
from time import sleep
from runtime_test import LogExecutionTime
from io import BytesIO

class CustomMicrophone(sr.Microphone):
    """
    A custom microphone class that extends the speech_recognition.Microphone class.

    This class sets a predefined sample rate for the microphone, ensuring consistent
    audio input quality for speech recognition.

    Inherits:
        sr.Microphone: The base Microphone class from the speech_recognition module.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the CustomMicrophone with a specific sample rate.
        """
        kwargs['sample_rate'] = 16000
        super(CustomMicrophone, self).__init__(*args, **kwargs)


class RecordVoice:
    """
    A class to handle voice recording and processing for speech-to-text conversion.

    This class utilizes the speech_recognition library to capture audio from the microphone
    and converts it to text using Google's speech recognition service. It also formats the
    recognized text to UCI chess format.

    Attributes:
        Recognize (sr.Recognizer): An instance of the Recognizer class for speech recognition.
        Mic (CustomMicrophone): An instance of the CustomMicrophone for audio input.
        formatting (formatting): An instance of the formatting class for UCI chess format conversion.
    """

    def __init__(self):
        """
        Initializes the RecordVoice class with necessary components for speech recognition.
        """
        self.Recognize = sr.Recognizer()
        self.Recognize.pause_threshold = 1.0
        self.Mic = CustomMicrophone()
        with CustomMicrophone() as source:
            # Adjust the recognizer sensitivity to ambient noise
            self.Recognize.adjust_for_ambient_noise(source)

    @LogExecutionTime
    def listen(self, phrase_timeout):
        """
        Listens for audio input and captures it for processing.

        Args:
            phrase_timeout (float, optional): Maximum duration for capturing a phrase.

        Returns:
            audio (AudioData): The captured audio data, or None if an error occurs.
        """
        try:
            with CustomMicrophone() as source:
                # print("Listening....")
                audio = self.Recognize.listen(source, 
                                            timeout=None, 
                                            phrase_time_limit=phrase_timeout)
                # print("Stop Listening....")
                # Export the AudioData to a byte stream

                wav_data = audio.get_wav_data() 
                return wav_data

                # return audio
        
        except sr.RequestError:
            # Handle errors related to the API or network issues
            print("API unavailable. Please check your internet connection")
            sleep(1)
            return None

    @LogExecutionTime
    def analyze(self, audio):
        """
        Analyzes the captured audio and converts it to text.

        This method utilizes Google's speech recognition service to convert the audio to text.
        The text is then formatted to UCI chess notation if possible.

        Args:
            audio (AudioData): The audio data to analyze.

        Returns:
            tuple: A tuple containing a boolean indicating if an error occurred, and the 
            converted text or an error message.
        """
        # audio_converted = sr.AudioData(audio, sample_rate=16000, sample_width=2)
        try:
            # if not isinstance(audio, sr.AudioData):
                # If not, convert it to AudioData (example shown for raw bytes)
            sound = sr.AudioData(audio, sample_rate=16000, sample_width=2)

            # text = self.Recognize.recognize_google(audio_converted)
            
            text = self.Recognize.recognize_google(sound)
            print(text)
            return text

        except sr.UnknownValueError:
            # Handle the case where speech is not recognized
            # print('\a')
            # print("Speech was not understood.")
            pass
        
        except sr.RequestError as e:
            # Handle API request errors
            # print(f"Could not request results from Google Speech Recognition service; {e}")
            pass