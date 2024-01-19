import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available TTS models
print(TTS().list_models())

base_path = '/Users/wiktoriamronga/TTS/resources/'

emotion_ref_dict = {
    'neutral': '01',
    'calm': '02',
    'happy': '03',
    'sad': '04',
    'angry': '05',
    'fearful': '06',
    'disgust': '07',
    'surprised': '08' 
}

def make_ref_path(emotion="neutral", gender="female", strong_intensity=False):
    if gender is "female":
        actor = "RAVDESS_Actor_02_(english+female)/"
        actor_id = '02'
    else:
        actor = "RAVDESS_Actor_21_(english+male)/"
        actor_id = '21'
    if strong_intensity:
        intensity = '02'
    else:
        intensity = '01' 
    return base_path + actor + '/03-01-' + emotion_ref_dict[emotion] + '-' + intensity + '-01-01-' + actor_id + '.wav'


# Initialize TTS
#tts = TTS("tts_models/en/ljspeech/glow-tts").to(device)

def emotional_tts(text_to_say, emotion="neutral", gender="female", strong_intensity=False, output_path="/Users/wiktoriamronga/TTS/output/ref1.wav"):
    
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    
    #emotion_reference="/Users/wiktoriamronga/TTS/resources/ref1.wav"
    emotion_reference = make_ref_path(emotion=emotion, gender=gender, strong_intensity=strong_intensity)
    # Run TTS
    # Text to speech list of amplitude values as output
    # wav = tts.tts(text=text_to_say, speaker_wav=emotion_reference, language="en")

    # Text to speech to a file
    tts.tts_to_file(text=text_to_say, speaker_wav=emotion_reference, language="en", file_path=output_path)

text="Hello, it's Victoria, and I am working on TTS."
emotional_tts(text)