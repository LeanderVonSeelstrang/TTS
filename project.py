import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available TTS models
print(TTS().list_models())

# Initialize TTS
#tts = TTS("tts_models/en/ljspeech/glow-tts").to(device)
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)



# Run TTS
# Text to speech list of amplitude values as output
wav = tts.tts(text="Hello, it's Victoria, and I am working on TTS.", speaker_wav="/Users/wiktoriamronga/TTS/References/ref1.wav", language="en")

# Text to speech to a file
tts.tts_to_file(text="Hello, it's Victoria, and I am working on TTS.", speaker_wav="/Users/wiktoriamronga/TTS/References/ref1.wav", language="en", file_path="/Users/wiktoriamronga/TTS/output/ref1.wav")
