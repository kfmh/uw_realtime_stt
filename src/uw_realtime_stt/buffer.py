import pyaudio
from pydub import AudioSegment, silence
from datetime import datetime
# from stt import RecordVoice
# import speech_recognition as sr 
from io import BytesIO
from distil_whisper import stt

class AudioRecorder:
    def __init__(self, buffer_duration=10000, silence_thresh=-30, silence_duration=2000, export_path='./'):
        self.buffer_duration = buffer_duration
        self.silence_thresh = silence_thresh
        self.silence_duration = silence_duration
        self.export_path = export_path
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.chunk_size = 1024
        self.stt =  stt()

    def export_audio(self, buffer, filename):
        """
        Export the audio buffer to a file.
        :param buffer: The AudioSegment buffer to export
        :param filename: The filename for the exported audio
        """
        buffer.export(filename, format='wav')

    def record(self):
        """
        Record audio in chunks, detect silence, export, and manage an audio buffer.
        """
        p = pyaudio.PyAudio()
        stream = p.open(format=self.audio_format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk_size)

        buffer = AudioSegment.silent(duration=0)

        try:
            while True:
                print("loop")
                frames = []
                for _ in range(0, int(self.rate / self.chunk_size)):
                    try:
                        data = stream.read(self.chunk_size)
                        frames.append(data)
                    except IOError as e:
                        if e.errno == pyaudio.paInputOverflowed:
                            continue

                chunk = AudioSegment(data=b''.join(frames), sample_width=p.get_sample_size(self.audio_format), frame_rate=self.rate, channels=self.channels)
                buffer += chunk
                
                if len(buffer) > self.buffer_duration:
                    buffer = buffer[-self.buffer_duration:]

                with BytesIO() as audio_io:
                    chunk.export(audio_io, format='wav')
                    wav_data = audio_io.read()
                self.stt.analyze(wav_data)

                # Check the last part of the buffer for silence
                if len(buffer) >= self.silence_duration and silence.detect_silence(buffer[-self.silence_duration:], min_silence_len=self.silence_duration, silence_thresh=self.silence_thresh):
                    print("Silence detected, exporting and flushing buffer")
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    self.export_audio(buffer, f'{self.export_path}recording_{timestamp}.wav')
                    buffer = AudioSegment.silent(duration=0)

        except KeyboardInterrupt:
            print("Recording stopped")
        finally:
            if stream.is_active():
                stream.stop_stream()
            stream.close()
            p.terminate()

# Example usage
recorder = AudioRecorder()
recorder.record()
