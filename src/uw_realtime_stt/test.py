import pyaudio
from pydub import AudioSegment, silence
from datetime import datetime
from multiprocessing import Process, Queue
from print_document import Create_Document
from time import sleep
from io import BytesIO
from distil_whisper import stt


buffer_duration=10000
silence_thresh = 30

silence_duration = 2000
export_path = "./"
audio_format = pyaudio.paInt16
channels = 1
rate = 44100
chunk_size = 1024

def export_audio(buffer, filename):
    """
    Export the audio buffer to a file.
    :param buffer: The AudioSegment buffer to export
    :param filename: The filename for the exported audio
    """
    buffer.export(filename, format='wav')

def process_analyze(name, queue):
    print(f"Start: {name}")


    while True:
        data = queue.get()
        if data == "STOP":
            break
        
        text = stt(data)
        print(text)

def process_rec(name, queue,):
    """
    Record audio in chunks, detect silence, export, and manage an audio buffer.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)

    buffer = AudioSegment.silent(duration=0)

    try:
        while True:
            frames = []
            for _ in range(0, int(rate / chunk_size)):
                try:
                    data = stream.read(chunk_size)
                    frames.append(data)
                except IOError as e:
                    if e.errno == pyaudio.paInputOverflowed:
                        continue

            chunk = AudioSegment(data=b''.join(frames), sample_width=p.get_sample_size(audio_format), frame_rate=rate, channels=channels)
            buffer += chunk

            if len(buffer) > buffer_duration:
                buffer = buffer[-buffer_duration:]

            with BytesIO() as audio_io:
                chunk.export(audio_io, format='wav')
                wav_data = audio_io.read()
            # stt.analyze(wav_data)
            text = queue.put(wav_data)
            print(text )

            # Check the last part of the buffer for silence
            if len(buffer) >= silence_duration and silence.detect_silence(buffer[-silence_duration:], min_silence_len=silence_duration, silence_thresh=silence_thresh):
                print("Silence detected, exporting and flushing buffer")
                # timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                # export_audio(buffer, f'{export_path}recording_{timestamp}.wav')
                buffer = AudioSegment.silent(duration=0)

    except KeyboardInterrupt:
        print("Recording stopped")
    finally:
        if stream.is_active():
            stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    print("starting")
    
    queue = Queue()
    
    p1 = Process(target=process_analyze, args=('analyze', queue))
    p2 = Process(target=process_rec, args=('rec1', queue))
    
    p1.start()
    p2.start()

    # Wait for the processes to finish (or handle them as needed)
    p1.join()
    p2.join()