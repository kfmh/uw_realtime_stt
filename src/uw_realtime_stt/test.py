from stt import STT
import wave
import numpy as np

stt = STT()

with wave.open('test.wav', 'r') as f:
# with wave.open('./audio_samples/audio1.wav', 'r') as f:
    # Get parameters
    n_channels, sample_width, framerate, n_frames, _, _ = f.getparams()
    print(n_channels)
    print(sample_width)
    print(framerate)
    print(n_frames)
    # Read frames
    audio_frames = f.readframes(n_frames)
    
    # Convert to numpy array (for mono audio)
    if sample_width == 2:
        audio_data = np.frombuffer(audio_frames, dtype=np.int16)
    elif sample_width == 4:
        audio_data = np.frombuffer(audio_frames, dtype=np.int32)


result = stt.analyse(audio_data)
print(result)