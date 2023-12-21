import sounddevice as sd
import numpy as np
import soundfile as sf
import threading
import os
VOICE_FOLDER = "voices"
stop_recording = False

def record_audio(name="user_input", input_device=None):
    local_dir_path = VOICE_FOLDER
    local_file_path = os.path.join(local_dir_path, f"{name}.wav")
    if not os.path.exists(local_dir_path):
        os.mkdir(local_dir_path)
    if input_device is None:
        input_device = sd.default.device["input"]

    print("Recording... Press Enter to stop.")

    # Create a thread to run the recording in the background
    recording_thread = threading.Thread(target=start_recording, args=(local_file_path, input_device))
    recording_thread.start()

    # Wait for the user to press Enter to stop recording
    input("Press Enter to stop recording.\n")

    # Signal the recording thread to stop
    global stop_recording
    stop_recording = True
    recording_thread.join()

    print(f"Recording saved to {local_file_path}")
    return local_file_path

def start_recording(file_path, input_device):
    global stop_recording
    stop_recording = False

    # Record audio until stop_recording is set to True
    with sd.InputStream(device=input_device, channels=1, dtype=np.int16) as stream:
        audio_data = []
        while not stop_recording:
            block, overflowed = stream.read(1024)
            audio_data.extend(block)

        # Convert audio_data to NumPy array
        audio_data = np.array(audio_data)

        sf.write(file_path, audio_data, int(stream.samplerate))

if __name__ == "__main__":
    record_audio()
