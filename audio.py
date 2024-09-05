import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import time


def record_audio(filename="E:\\output.wav", sample_rate=44100):
    print("Recording started... Press Ctrl+C to stop.")

    # Create a list to hold recorded audio chunks
    recorded_audio = []

    try:
        while True:
            # Record audio in 1-second chunks
            recording = sd.rec(int(1 * sample_rate), samplerate=sample_rate, channels=2, dtype=np.int16)
            sd.wait()  # Wait until the chunk is recorded

            # Append the chunk to the list of recordings
            recorded_audio.append(recording)

    except KeyboardInterrupt:
        print("Recording stopped by user.")

    # Concatenate all recorded chunks into a single array
    recorded_audio = np.concatenate(recorded_audio, axis=0)

    # Save the recording to a WAV file
    wav.write(filename, sample_rate, recorded_audio)
    print(f"Recording saved as {filename}")


if __name__ == "__main__":
    record_audio()
