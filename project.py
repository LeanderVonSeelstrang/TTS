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
    '''
    Class to generate emotional TTS using the TTS API

    Attributes:
    tts: TTS object
        TTS object to generate TTS
    base_path: str
        Base path for the resources
    output_base_path: str
        Base path for the output
    emotion_ref_dict: dict
        Dictionary to map emotions to the reference file
            neutral
            calm
            happy
            sad
            angry
            fearful
            disgust
            surprised

    Methods:
    make_ref
        Method to generate the reference file path
    emotional_tts
        Method to generate the emotional TTS
    '''
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

    def make_ref_path(self, 
                      emotion="neutral", 
                      gender="female", 
                      strong_intensity=False):
        '''
        Method to generate the reference file path
        '''

        if emotion not in self.emotion_ref_dict:
            print("Invalid emotion")
            print("Available emotions: ", self.emotion_ref_dict.keys())
            raise ValueError("Invalid emotion")
        if emotion == "neutral" and strong_intensity:
            raise ValueError("Strong intensity not available for neutral emotion")
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
    parser.add_argument("--emotion", type=str, default="neutral", choices=emotion_ref_dict.keys(), help="Emotion for TTS (default: neutral)")
    parser.add_argument("--gender", type=str, default="female", choices=["female", "male"], help="Gender for TTS (default: female)")
    parser.add_argument("--strong_intensity", action="store_true", help="Flag: Use strong intensity for emotion")
    parser.add_argument("--output_path", type=str, default="output.wav", help="Output file path (default: output.wav)")
    parser.add_argument("--as_command_line_tool", action="store_true", help="Use as command line tool (default: False)")

    return parser.parse_args()


def main():
    args = parse_arguments()

    if args.as_command_line_tool:
        # Generate output path
        tts_path = pathlib.Path(__file__).parent.resolve()
        output_base_path = os.path.join(tts_path, "output/")
        output_path = output_base_path + args.output_path
        print("Generating TTS with emotion: ", args)
        e_tts = EmotionalTts()
        # Generate TTS
        e_tts.emotional_tts(args.text, args.emotion, args.gender, args.strong_intensity, output_path, None)
    else:
        print("Command line usage is deactivated. Use --as_command_line_tool flag to use as command line tool. If you are using it as a module you can igoore this message.")

if __name__ == "__main__":
    main()
    
# Example Usage
# python project.py "Testing the emotional TTS command line tool." --emotion happy --gender female --output_path happy_output.wav --as_command_line_tool
# python project.py "Ewww. Testing the emotional TTS command line tool." --emotion disgust --gender male --output_path disgust_output.wav --strong_intensity --as_command_line_tool

'''
python project.py "This is neutral" --emotion neutral --gender female --output_path neutral__female.wav --as_command_line_tool
python project.py "This is neutral" --emotion neutral --gender male --output_path neutral__male.wav --as_command_line_tool
python project.py "This is calm" --emotion calm --gender female --output_path calm__female.wav --as_command_line_tool
python project.py "This is calm" --emotion calm --gender male --output_path calm__male.wav --as_command_line_tool
python project.py "This is happy" --emotion happy --gender female --output_path happy__female.wav --as_command_line_tool
python project.py "This is happy" --emotion happy --gender male --output_path happy__male.wav --as_command_line_tool
python project.py "This is sad" --emotion sad --gender female --output_path sad__female.wav --as_command_line_tool
python project.py "This is sad" --emotion sad --gender male --output_path sad__male.wav --as_command_line_tool
python project.py "This is angry" --emotion angry --gender female --output_path angry__female.wav --as_command_line_tool
python project.py "This is angry" --emotion angry --gender male --output_path angry__male.wav --as_command_line_tool
python project.py "This is fearful" --emotion fearful --gender female --output_path fearful_female.wav --as_command_line_tool
python project.py "This is fearful" --emotion fearful --gender male --output_path fearful_male.wav --as_command_line_tool
python project.py "This is disgust" --emotion disgust --gender female --output_path disgust__female.wav --as_command_line_tool
python project.py "This is disgust" --emotion disgust --gender male --output_path disgust__male.wav --as_command_line_tool
python project.py "This is surprised" --emotion surprised --gender female --output_path surprised__female.wav --as_command_line_tool
python project.py "This is surprised" --emotion surprised --gender male --output_path surprised__male.wav --as_command_line_tool

python project.py "This is very calm" --emotion calm --strong_intensity --gender female --output_path calm_strongIntensity__female.wav --as_command_line_tool
python project.py "This is very calm" --emotion calm --strong_intensity --gender male --output_path calm_strongIntensity__male.wav --as_command_line_tool
python project.py "This is very happy" --emotion happy --strong_intensity --gender female --output_path happy_strongIntensity__female.wav --as_command_line_tool
python project.py "This is very happy" --emotion happy --strong_intensity --gender male --output_path happy_strongIntensity__male.wav --as_command_line_tool
python project.py "This is very sad" --emotion sad --strong_intensity --gender female --output_path sad_strongIntensity__female.wav --as_command_line_tool
python project.py "This is very sad" --emotion sad --strong_intensity --gender male --output_path sad_strongIntensity__male.wav --as_command_line_tool
python project.py "This is very angry" --emotion angry --strong_intensity --gender female --output_path angry_strongIntensity__female.wav --as_command_line_tool
python project.py "This is very angry" --emotion angry --strong_intensity --gender male --output_path angry_strongIntensity__male.wav --as_command_line_tool
python project.py "This is very fearful" --emotion fearful --strong_intensity --gender female --output_path fearful_strongIntensity__female.wav --as_command_line_tool
python project.py "This is very fearful" --emotion fearful --strong_intensity --gender male --output_path fearful_strongIntensity__male.wav --as_command_line_tool
python project.py "This is very disgust" --emotion disgust --strong_intensity --gender female --output_path disgust_strongIntensity__female.wav --as_command_line_tool
python project.py "This is very disgust" --emotion disgust --strong_intensity --gender male --output_path disgust_strongIntensity__male.wav --as_command_line_tool
python project.py "This is very surprised" --emotion surprised --strong_intensity --gender female --output_path surprised_strongIntensity__female.wav --as_command_line_tool
python project.py "This is very surprised" --emotion surprised --strong_intensity --gender male --output_path surprised_strongIntensity__male.wav --as_command_line_tool
'''


'''
Speed on M2 Macbook Air

Generating TTS with emotion:  Namespace(text='This is neutral', emotion='neutral', gender='female', strong_intensity=False, output_path='neutral__female.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is neutral']
 > Processing time: 2.999390125274658
 > Real-time factor: 1.4508720661264085
Generating TTS with emotion:  Namespace(text='This is neutral', emotion='neutral', gender='male', strong_intensity=False, output_path='neutral__male.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is neutral']
 > Processing time: 6.447139263153076
 > Real-time factor: 1.559586413381224
Generating TTS with emotion:  Namespace(text='This is calm', emotion='calm', gender='female', strong_intensity=False, output_path='calm__female.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is calm']
 > Processing time: 3.1597471237182617
 > Real-time factor: 1.5725989544507872
Generating TTS with emotion:  Namespace(text='This is calm', emotion='calm', gender='male', strong_intensity=False, output_path='calm__male.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is calm']
 > Processing time: 6.4242448806762695
 > Real-time factor: 1.5540481790735448
Generating TTS with emotion:  Namespace(text='This is happy', emotion='happy', gender='female', strong_intensity=False, output_path='happy__female.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is happy']
 > Processing time: 3.1658689975738525
 > Real-time factor: 1.5314016189124133
Generating TTS with emotion:  Namespace(text='This is happy', emotion='happy', gender='male', strong_intensity=False, output_path='happy__male.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is happy']
 > Processing time: 6.146970987319946
 > Real-time factor: 1.6237865424382407
Generating TTS with emotion:  Namespace(text='This is sad', emotion='sad', gender='female', strong_intensity=False, output_path='sad__female.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is sad']
 > Processing time: 2.864612102508545
 > Real-time factor: 1.4594430882697185
Generating TTS with emotion:  Namespace(text='This is sad', emotion='sad', gender='male', strong_intensity=False, output_path='sad__male.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is sad']
 > Processing time: 3.9401209354400635
 > Real-time factor: 1.5351934306342485
Generating TTS with emotion:  Namespace(text='This is angry', emotion='angry', gender='female', strong_intensity=False, output_path='angry__female.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is angry']
 > Processing time: 3.207137107849121
 > Real-time factor: 1.4767242989490712
Generating TTS with emotion:  Namespace(text='This is angry', emotion='angry', gender='male', strong_intensity=False, output_path='angry__male.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is angry']
 > Processing time: 2.4590749740600586
 > Real-time factor: 1.5799126800123626
Generating TTS with emotion:  Namespace(text='This is fearful', emotion='fearful', gender='female', strong_intensity=True, output_path='fearful_strongIntensity_female.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is fearful']
 > Processing time: 2.6719810962677
 > Real-time factor: 1.56494855431106
Generating TTS with emotion:  Namespace(text='This is fearful', emotion='fearful', gender='male', strong_intensity=True, output_path='fearful_strongIntensity_male.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is fearful']
 > Processing time: 3.988922119140625
 > Real-time factor: 1.5828486309935714
Generating TTS with emotion:  Namespace(text='This is disgust', emotion='disgust', gender='female', strong_intensity=False, output_path='disgust__female.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is disgust']
 > Processing time: 3.338228940963745
 > Real-time factor: 1.5370854524776683
Generating TTS with emotion:  Namespace(text='This is disgust', emotion='disgust', gender='male', strong_intensity=False, output_path='disgust__male.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is disgust']
 > Processing time: 5.946073770523071
 > Real-time factor: 1.5707174458505095
Generating TTS with emotion:  Namespace(text='This is surprised', emotion='surprised', gender='female', strong_intensity=False, output_path='surprised__female.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is surprised']
 > Processing time: 3.0807149410247803
 > Real-time factor: 1.6075767808026413
Generating TTS with emotion:  Namespace(text='This is surprised', emotion='surprised', gender='male', strong_intensity=False, output_path='surprised__male.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is surprised']
 > Processing time: 4.1949639320373535
 > Real-time factor: 1.5437075217193532

 Generating TTS with emotion:  Namespace(text='This is very calm', emotion='calm', gender='female', strong_intensity=True, output_path='calm_strongIntensity__female.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is very calm']
 > Processing time: 4.0672807693481445
 > Real-time factor: 1.64424209746492
Generating TTS with emotion:  Namespace(text='This is very calm', emotion='calm', gender='male', strong_intensity=True, output_path='calm_strongIntensity__male.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is very calm']
 > Processing time: 6.996451139450073
 > Real-time factor: 1.6328508427696242
Generating TTS with emotion:  Namespace(text='This is very happy', emotion='happy', gender='female', strong_intensity=True, output_path='happy_strongIntensity__female.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is very happy']
 > Processing time: 3.010561943054199
 > Real-time factor: 1.4983498294588546
Generating TTS with emotion:  Namespace(text='This is very happy', emotion='happy', gender='male', strong_intensity=True, output_path='happy_strongIntensity__male.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is very happy']
 > Processing time: 4.320921182632446
 > Real-time factor: 1.4765111591409223
Generating TTS with emotion:  Namespace(text='This is very sad', emotion='sad', gender='female', strong_intensity=True, output_path='sad_strongIntensity__female.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is very sad']
 > Processing time: 2.695906162261963
 > Real-time factor: 1.4507206871797218
Generating TTS with emotion:  Namespace(text='This is very sad', emotion='sad', gender='male', strong_intensity=True, output_path='sad_strongIntensity__male.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is very sad']
 > Processing time: 5.220901966094971
 > Real-time factor: 1.544997964789485
Generating TTS with emotion:  Namespace(text='This is very angry', emotion='angry', gender='female', strong_intensity=True, output_path='angry_strongIntensity__female.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is very angry']
 > Processing time: 3.618659257888794
 > Real-time factor: 1.498036884883747
Generating TTS with emotion:  Namespace(text='This is very angry', emotion='angry', gender='male', strong_intensity=True, output_path='angry_strongIntensity__male.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is very angry']
 > Processing time: 2.8468849658966064
 > Real-time factor: 1.4855597666135028
Generating TTS with emotion:  Namespace(text='This is very fearful', emotion='fearful', gender='female', strong_intensity=True, output_path='fearful_strongIntensity__female.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is very fearful']
 > Processing time: 3.515842914581299
 > Real-time factor: 1.4840033741676424
Generating TTS with emotion:  Namespace(text='This is very fearful', emotion='fearful', gender='male', strong_intensity=True, output_path='fearful_strongIntensity__male.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is very fearful']
 > Processing time: 5.695544004440308
 > Real-time factor: 1.5279679932099084
Generating TTS with emotion:  Namespace(text='This is very disgust', emotion='disgust', gender='female', strong_intensity=True, output_path='disgust_strongIntensity__female.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is very disgust']
 > Processing time: 3.8486950397491455
 > Real-time factor: 1.4995710635154909
Generating TTS with emotion:  Namespace(text='This is very disgust', emotion='disgust', gender='male', strong_intensity=True, output_path='disgust_strongIntensity__male.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is very disgust']
 > Processing time: 6.216830015182495
 > Real-time factor: 1.560861516610198
Generating TTS with emotion:  Namespace(text='This is very surprised', emotion='surprised', gender='female', strong_intensity=True, output_path='surprised_strongIntensity__female.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is very surprised']
 > Processing time: 3.354177951812744
 > Real-time factor: 1.544429164664864
Generating TTS with emotion:  Namespace(text='This is very surprised', emotion='surprised', gender='male', strong_intensity=True, output_path='surprised_strongIntensity__male.wav', as_command_line_tool=True)
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
 > Text splitted to sentences.
['This is very surprised']
 > Processing time: 5.381742715835571
 > Real-time factor: 1.5925948422290954
'''