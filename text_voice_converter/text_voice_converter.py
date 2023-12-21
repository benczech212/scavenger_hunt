from pydub import AudioSegment
from pydub.playback import play

from pathlib import Path
from openai import OpenAI
import os
import sounddevice as sd
import numpy as np

VOICE_FOLDER = "voices" 
WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_VOICE = "alloy"

def create_gpt_client():
    with open('/etc/OPENAI_API_KEY', 'r') as file:
        api_key = file.read().strip()
    return  OpenAI(api_key=api_key)


def create_speech_from_text(text, model="tts-1", voice=DEFAULT_VOICE, file_path="agent_voice.mp3"):
    client = create_gpt_client()
    os.mkdir(VOICE_FOLDER)
    local_path = os.path.join(VOICE_FOLDER, file_path)
    full_path = os.path.join(WORKING_DIR, local_path)

    # Generate speech from text
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
    )
    
    response.stream_to_file(full_path)
    # Save the speech to the specified file path
    
    return local_path

def play_audio(file_path):
    # Load the audio file
    audio = AudioSegment.from_mp3(file_path)

    # Play the audio
    play(audio)

def list_audio_devices():
    print("Available audio devices:")
    for i, device_info in enumerate(sd.query_devices()):
        print(f"{i}: {device_info['name']}")

def record_audio(file_path="user_input.wav", duration=5, sample_rate=44100):
    print("Recording... Speak now!")

    # Record audio from the microphone
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.int16)
    sd.wait()

    # Save the recorded audio to a file
    sd.write(file_path, audio_data, sample_rate)


    print(f"Recording saved to {file_path}")

def convert_wav_to_mp3(file_name="user_input", output_file="user_input.mp3"):
    file_path = f"{file_name}.mp3"
    os.mkdir(VOICE_FOLDER)
    local_path = os.path.join(VOICE_FOLDER, file_path)
    full_path = os.path.join(WORKING_DIR, local_path)
    # Load the recorded audio
    audio = AudioSegment.from_wav(full_path)

    # Save as MP3
    audio.export(output_file, format="mp3")
    print(f"Conversion complete. MP3 file saved to {output_file}")

def convert_wav_to_mp3(input_file):
    # Load the recorded audio
    output_file = input_file.replace(".wav", ".mp3")
    audio = AudioSegment.from_wav(input_file)

    # Save as MP3
    audio.export(output_file, format="mp3")
    print(f"Conversion complete. MP3 file saved to {output_file}")
    print("Deleting WAV file...")
    os.remove(input_file)

# # Example usage:
# record_audio("user_input.wav", duration=5)

# # Example usage:
# text_to_speak = "Today is a wonderful day to build something people love!"
# agent_voice_file = create_speech_from_text(text_to_speak)
# play_audio(agent_voice_file)


list_audio_devices()

