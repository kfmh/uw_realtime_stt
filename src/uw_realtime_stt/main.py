from .print_document import Create_Document
from .stt import STT
from multiprocessing import Process, Queue
from time import sleep
import pyaudio
from pydub import AudioSegment, silence
from datetime import datetime


def export_audio(buffer, filename):
    """
    Export the audio buffer to a file.
    :param buffer: The AudioSegment buffer to export
    :param filename: The filename for the exported audio
    """
    buffer.export(filename, format='wav')

def process_analyze(name, queue):
    print(f"Start: {name}")
    stt = STT()
    printing = Create_Document()
    while True:
        data = queue.get()
        if data == "STOP":
            break

        # Process and analyze the audio data
        text = stt.analyse(data[0])

        printing.document(text, data[1])

def process_rec(name, queue):
    print(f"Start: {name}")
    silence_thresh = -30
    silence_duration = 1000
    export_path = './test_audio/'
    audio_format = pyaudio.paInt16
    channels = 1
    rate = 22050
    chunk_size = 2048
    record_duration = 0.5
    p = pyaudio.PyAudio()
    stream = p.open(format=audio_format, 
                    channels=channels, 
                    rate=rate, input=True, 
                    frames_per_buffer=chunk_size)

    buffer = AudioSegment.silent(duration=0)
    accumulated_duration = 0

    while True:
        # data =  recorder.record()
        flushing = False
        frames = []
        for _ in range(0, int(rate / chunk_size * record_duration)): # Record for 1 second
            try:
                data = stream.read(chunk_size)
                frames.append(data)
            except IOError as e:
                if e.errno == pyaudio.paInputOverflowed:
                    continue

        chunk = AudioSegment(data=b''.join(frames), 
                             sample_width=p.get_sample_size(audio_format), 
                             frame_rate=rate, 
                             channels=channels)
        buffer += chunk
        accumulated_duration += len(chunk)
        data = buffer.raw_data

        if len(buffer) >= silence_duration and silence.detect_silence(buffer[-silence_duration:], min_silence_len=silence_duration, silence_thresh=silence_thresh):
            # print("Silence detected, exporting and flushing buffer")
            # timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            # export_audio(buffer, f'{export_path}r_{timestamp}.wav')
            buffer = AudioSegment.silent(duration=0)
            flushing = True

        queue.put((data, flushing))  # Put recorded data into the queue
    
def main():
    print("starting")
    
    queue = Queue()
    
    p1 = Process(target=process_analyze, args=('analyze', queue))
    p2 = Process(target=process_rec, args=('rec1', queue,))
    
    p1.start()
    p2.start()

    try:
        # Wait for the processes to finish (or handle them as needed)
        p1.join()
        p2.join()
    except KeyboardInterrupt:
        print("Interrupted by user, shutting down...")
        # Send stop signal to the processes
        queue.put("STOP")
        p1.terminate()
        p2.terminate()
        p1.join()
        p2.join()
        print("Processes terminated successfully.")

if __name__ == "__main__":
    main()