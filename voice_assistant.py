import openai
import sounddevice as sd
import soundfile as sf
import os
import threading
from pathlib import Path
from  gtp_client import *

# Set your OpenAI API key here
openai.api_key = get_api_key()

VOICE_FOLDER = "voices"
stop_recording = False

def create_assistant(instructions, name, model="gpt-4"):
    assistant = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": instructions},
        ],
        max_tokens=1500,
    )
    return assistant["id"]

def text_to_voice(text, file_name="assistant_voice"):
    response = openai.TextToSpeech.create(
        text=text,
        model="tts-1",
        voice="alloy",
    )
    file_path = os.path.join(VOICE_FOLDER, f"{file_name}.mp3")
    response.stream_to_file(file_path)
    return file_path

def play_audio(file_path):
    os.system(f"start {file_path}")

def record_audio(file_name="user_input", input_device=None):
    local_dir_path = VOICE_FOLDER
    local_file_path = os.path.join(local_dir_path, f"{file_name}.wav")
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
    with sd.InputStream(device=input_device, channels=1, dtype="int16") as stream:
        audio_data = []
        while not stop_recording:
            block, overflowed = stream.read(1024)
            audio_data.extend(block)

        # Convert audio_data to NumPy array
        audio_data = np.array(audio_data)

        sf.write(file_path, audio_data, stream.samplerate)

def main():
    instructions = "You are a wizard shop owner. I will be connecting you with Sabrina, my beautiful girlfriend. You are to give her riddles that she is to complete. The first should be easy, the second one hard, and the third one even harder. She loves English, alliteration, logic, and fantasy. Let her know she can ask for clues and hints. Don't let her know the answers even if she asks. When she gets all three correct, reveal the secret link {result_link}. Wait for her to ask you the first question before responding."
    assistant_id = create_assistant(instructions, "Merlin Mystique")

    assistant_voice_text = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "assistant", "content": "Hello, I am Merlin Mystique."},
        ],
        max_tokens=1500,
    )["choices"][0]["message"]["content"]

    assistant_voice_file = text_to_voice(assistant_voice_text, "assistant_voice")
    play_audio(assistant_voice_file)

    input("Press Enter when ready to start recording.\n")

    user_input_file = record_audio("user_input")
    user_input_text = openai.TextToSpeech.create(
        file=Path(user_input_file).open("rb"),
        model="whisper-1",
        voice="hush",
    )["text"]

    # Send user_input_text to assistant and continue the conversation...
    print(user_input_text)

if __name__ == "__main__":
    main()
