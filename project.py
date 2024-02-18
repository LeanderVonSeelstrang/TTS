import torch
from TTS.api import TTS
import argparse

import pathlib
import os

class EmotionalTts(object):

    # Get device
    def __init__(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        # Initialize TTS
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

        # List available TTS models
        # print(TTS().list_models())

        tts_path = pathlib.Path(__file__).parent.resolve()

        self.base_path = os.path.join(tts_path, "resources/")    
        self.output_base_path = os.path.join(tts_path, "output/")

        self.emotion_ref_dict = {
            'neutral': '01',
            'calm': '02',
            'happy': '03',
            'sad': '04',
            'angry': '05',
            'fearful': '06',
            'disgust': '07',
            'surprised': '08' 
        }

    def make_ref_path(self, emotion="neutral", gender="female", strong_intensity=False):
        if gender == "female":
            actor = "RAVDESS_Actor_02_(english+female)/"
            actor_id = '02'
        else:
            actor = "RAVDESS_Actor_21_(english+male)/"
            actor_id = '21'
        if strong_intensity:
            intensity = '02'
        else:
            intensity = '01' 
        return self.base_path + actor + '/03-01-' + self.emotion_ref_dict[emotion] + '-' + intensity + '-01-01-' + actor_id + '.wav'


    def emotional_tts(self, 
                      text_to_say, 
                      emotion="neutral", 
                      gender="female", 
                      strong_intensity=False, 
                      output_path=" ~/emotional_TTS_output/output/output.wav", 
                      tts_module=None):
        if tts_module is None:
            tts_module=self.tts
        # Get reference audio file path
        emotion_reference = self.make_ref_path(emotion=emotion, gender=gender, strong_intensity=strong_intensity)
        # Text to speech to a file
        tts_module.tts_to_file(text=text_to_say, speaker_wav=emotion_reference, language="en", file_path=output_path)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Emotional TTS Command Line Tool")
    parser.add_argument("text", type=str, help="Text to be converted to speech")
    parser.add_argument("--emotion", type=str, default="neutral", choices=EmotionalTts.emotion_ref_dict.keys(), help="Emotion for TTS (default: neutral)")
    parser.add_argument("--gender", type=str, default="female", choices=["female", "male"], help="Gender for TTS (default: female)")
    parser.add_argument("--intensity", action="store_true", help="Use strong intensity for emotion")
    parser.add_argument("--output-path", type=str, default="output.wav", help="Output file path (default: output.wav)")

    return parser.parse_args()


def main():
    args = parse_arguments()

    # Generate output path
    output_path = EmotionalTts.output_base_path + args.output_path

    # Set to true if you want to use it as a command line tool
    if False:
        print("Generating TTS with emotion: ", args)
        # Generate TTS
        EmotionalTts.emotional_tts(args.text, args.emotion, args.gender, args.intensity, output_path, EmotionalTts.tts)

if __name__ == "__main__":
    main()
    
# Example Usage
# python project.py "Testing the emotional TTS command line tool." --emotion happy --gender female --output-path happy_output.wav
    
# python project.py "Ewww. Testing the emotional TTS command line tool." --emotion disgust --gender male --output-path disgust_output.wav --intensity