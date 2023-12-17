

from multiprocessing import Process, Queue
from buffer import RecordVoice  # Assuming RecordVoice is in record_voice.py
from print_document import Create_Document
from time import sleep


def process_analyze(name, queue):
    print(f"Start: {name}")
    stt = RecordVoice()

    while True:
        data = queue.get()
        if data == "STOP":
            break

        stt.add_to_buffer(data)
        audio_data = stt.get_from_buffer()

        if audio_data:
            # Process and analyze the audio data
            text = stt.analyze(audio_data)
            print(text)
            # Further processing or document creation based on the text
            # ...

def process_rec(name, queue, delay, process):
    sleep(delay)
    print(f"Start: {name} Time-delay: {delay}")
    recorder = RecordVoice()

    while True:
        data = recorder.listen(4, process)  # Record for 4 seconds
        queue.put(data)  # Put recorded data into the queue



if __name__ == "__main__":
    print("starting")
    
    queue = Queue()
    
    p1 = Process(target=process_analyze, args=('analyze', queue))
    p2 = Process(target=process_rec, args=('rec1', queue, 0, 1))
    p3 = Process(target=process_rec, args=('rec2', queue, 2,2))
    
    p1.start()
    p2.start()
    p3.start()

    # Wait for the processes to finish (or handle them as needed)
    p1.join()
    p2.join()
    p3.join()
