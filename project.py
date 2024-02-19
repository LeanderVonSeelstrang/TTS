import torch
from TTS.api import TTS
import argparse

import pathlib
import os

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
    #e_tts = EmotionalTts()
    parser = argparse.ArgumentParser(description="Emotional TTS Command Line Tool")
    parser.add_argument("text", type=str, help="Text to be converted to speech")
    parser.add_argument("--emotion", type=str, default="neutral", choices=emotion_ref_dict.keys(), help="Emotion for TTS (default: neutral)")
    parser.add_argument("--gender", type=str, default="female", choices=["female", "male"], help="Gender for TTS (default: female)")
    parser.add_argument("--intensity", action="store_true", help="Use strong intensity for emotion")
    parser.add_argument("--output_path", type=str, default="output.wav", help="Output file path (default: output.wav)")
    parser.add_argument("--as_command_line_tool", action="store_true", help="Use as command line tool (default: False)")

    return parser.parse_args()


def main():
    args = parse_arguments()    
    # Generate output path
    tts_path = pathlib.Path(__file__).parent.resolve()

    base_path = os.path.join(tts_path, "resources/")    
    output_base_path = os.path.join(tts_path, "output/")
    output_path = output_base_path + args.output_path

    # Set to true if you want to use it as a command line tool
    if args.as_command_line_tool:
        print("Generating TTS with emotion: ", args)
        e_tts = EmotionalTts()
        # Generate TTS
        e_tts.emotional_tts(args.text, args.emotion, args.gender, args.intensity, output_path, None) #e_tts.tts)

if __name__ == "__main__":
    main()
    
# Example Usage
# python project.py "Testing the emotional TTS command line tool." --emotion happy --gender female --output_path happy_output.wav --as_command_line_tool
    
# python project.py "Ewww. Testing the emotional TTS command line tool." --emotion disgust --gender male --output_path disgust_output.wav --intensity --as_command_line_tool