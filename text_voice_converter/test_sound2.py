import pyaudio
import wave

def list_audio_devices():
    p = pyaudio.PyAudio()
    print("Available audio devices:")
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        print(f"{i}: {info['name']}")

def record_audio(file_path="user_input.wav", duration=5, sample_rate=44100, device_id=None):
    print("Recording... Speak now!")

    # Open stream
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    input=True,
                    input_device_index=device_id,
                    frames_per_buffer=int(sample_rate * duration))

    # Record audio
    frames = []
    for _ in range(int(sample_rate / duration)):
        data = stream.read(int(sample_rate * duration))
        frames.append(data)

    # Stop the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio to a file
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"Recording saved to {file_path}")

# List available audio devices
list_audio_devices()

# Use the appropriate device ID (replace 0 with the desired device ID)
device_id = 0

# Record audio using the specified device
record_audio("user_input.wav", duration=5, device_id=device_id)
