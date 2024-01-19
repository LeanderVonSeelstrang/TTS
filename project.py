import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available TTS models
print(TTS().list_models())

base_path = '/Users/wiktoriamronga/TTS/resources/RAVDESS_Actor_02'

def make_base_ref_path(gender="female", strong_intensity=False):
    
    return base_path + '/03-'
    

emotion_ref_dict = {
    'neutral': ,
    'calm': ,
    'happy': ,
    'sad': ,
    'angry': ,
    'fearful': ,
    'disgust': ,
    'surprised': 
}

strong_emotion_ref_dict = {
    'neutral': ,
    'calm': ,
    'happy': ,
    'sad': ,
    'angry': ,
    'fearful': ,
    'disgust': ,
    'surprised': 
}

# Initialize TTS
#tts = TTS("tts_models/en/ljspeech/glow-tts").to(device)

def emotional_tts(text_to_say, emotion="neutral", gender="female", strong_intensity=False, output_path="/Users/wiktoriamronga/TTS/output/ref1.wav"):
    
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    
    emotion_reference="/Users/wiktoriamronga/TTS/resources/ref1.wav"
    # Run TTS
    # Text to speech list of amplitude values as output
    # wav = tts.tts(text=text_to_say, speaker_wav=emotion_reference, language="en")

    # Text to speech to a file
    tts.tts_to_file(text=text_to_say, speaker_wav=emotion_reference, language="en", file_path=output_path)

text="Hello, it's Victoria, and I am working on TTS."
emotional_tts(text)