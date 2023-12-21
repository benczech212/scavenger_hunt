import sounddevice as sd

def list_audio_devices():
    print("Available audio devices:")
    for i, device_info in enumerate(sd.query_devices()):
        print(f"{i}: {device_info['name']}")

# List available audio devices
list_audio_devices()
