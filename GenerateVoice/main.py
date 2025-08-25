from elevenlabs.client import ElevenLabs
from .log.logger import Logger
from dotenv import load_dotenv

import os
import json
import requests
import tempfile
import subprocess

import io
from pydub import AudioSegment

from espeakng import Speaker

CURRENT_PATH_FILE = os.path.abspath(__file__)
CURRENT_PATH = os.path.dirname(CURRENT_PATH_FILE)

load_dotenv(dotenv_path=fr"{CURRENT_PATH}\..\.env")

"""
DOCUMENTATION:

This VoiceGenerator uses Elevenlabs API:
Website: https://elevenlabs.io/

API Documentation: https://elevenlabs.io/docs/api-reference/introduction

You do not have a way to check if the API is still valid, you'll get an answer from the generate_voice() function to check if is not available anymore.

9BWtsMINqrJLrRacOk9x
"""

class AIGenerateVoice(object):
    
    """
    Class to generate voices from text 
    """

    def __init__(self, api_key: str, voice_id: str = "9BWtsMINqrJLrRacOk9x", model_id: str = None) -> None:

        self.api_key = api_key
        self.lab = ElevenLabs(api_key = api_key)
        self.voice_id = voice_id
        self.model_id = model_id

        self.success_logger = Logger(f"{CURRENT_PATH}/log/access.log")
        self.error_logger = Logger(f"{CURRENT_PATH}/log/errors.log")

        self.APIs = self.load_apis()

    def load_apis(self) -> dict:
        """

        Method to load all APIs

        """

        try:
            if "apis.json" in os.listdir(CURRENT_PATH):
                with open(fr"{CURRENT_PATH}\apis.json", "r") as file:
                    try:
                        return json.load(file)  # Proper way to load from a file
                    except json.JSONDecodeError:
                        return {}  # Handle corrupted/empty file
                    finally:
                        file.close()
            else:
                data = {}
                with open(fr"{CURRENT_PATH}\apis.json", "w") as file:
                    json.dump(data, file, indent=4)

                    file.close()
                self.success_logger.create_success_log(
                    "File apis.json created successfully. [object] GenerateVoice [method] load_apis()")

                return {}

        except Exception as error:

            self.error_logger.create_error_log(f"Error occurred trying to load APIs. [object] GenerateVoice [method] load_apis()\nError: {error}")

            return {}


    def generate_voice(self, text :  str) -> list:

        """
        
        Method to generate the voice from text
        
        :param: text - the script for the voice

        """

        try:
            
            audio_stream = self.lab.text_to_speech.stream(
                text=text,
                voice_id=self.voice_id,
            )

            self.success_logger.create_success_log("Audio voice succesfully created. [object] GenerateVoice [method] generate_voice()")

            return [{"audio_object" : audio_stream
            }, 200]


        except Exception as error:
            
            self.error_logger.create_error_log(f"Error occurred: {str(error)}. [object] GenerateVoice [method] generate_voice()")

            return [{"error" : str(error)
            } , 400]



    def get_all_voices(self) -> list:

        try:
            api_url = self.APIs['voices']

            headers = {"xi-api-key" : self.api_key}

            response = requests.get(api_url, headers= headers)

            if response.status_code == 200:

                json_content = json.loads(response.content.decode())

                return json_content

            else:


                return [{"error": "Unknown error"}, 400]

        except Exception as error:

            self.error_logger.create_error_log(
                f"Error occurred: {str(error)}. [object] GenerateVoice [method] generate_voice()")

            return [{"error": str(error)
                     }, 400]


    def write_out_voice(self, binary_content : bytes, output_path : str = None) -> list:
        """
        
        Method to write out an .mp3 file

        """
        if output_path is None:
            output_path = "output.mp3"

        try:

            with open(output_path, "wb") as f:
                
                for binary_data in binary_content:
                    if isinstance(binary_data, bytes):
                        f.write(binary_data)

                f.close()

            self.success_logger.create_success_log("Audio voice file successfully created. [object] GenerateVoice [method] write_out_voice()")

            return [{}, 200]

        except Exception as error:

            self.error_logger.create_error_log(f"Error occurred: {str(error)}. [object] GenerateVoice [method] write_out_voice()")

            return [{"error" : str(error)
            } , 400]

class ManualGenerateVoice:
    def __init__(self) -> None:
        self.success_logger = Logger(f"{CURRENT_PATH}/log/access.log")
        self.error_logger = Logger(f"{CURRENT_PATH}/log/errors.log")
        self.esng = Speaker()

    def generate_voice(self, text: str, voice: str = "ro") -> list:
        """
        Generează audio din text și returnează datele audio în format bytes.

        Args:
            text (str): Textul de convertit în vorbire.
            voice (str): Numele vocii utilizate pentru sinteză.

        Returns:
            bytes: Datele audio generate.
        """
        try:
            # Setează vocea
            self.esng.voice = voice

            # Generează audio în format WAV
            audio_data = self.esng.speak(text)

            # Crează un buffer în memorie pentru a stoca datele audio
            audio_buffer = io.BytesIO(audio_data)

            return [{"audio_object": audio_buffer.read()}, 200]

        except Exception as error:
            self.error_logger.create_error_log(
                f"Exception: {str(error)}. [object] ManualGenerateVoice [method] generate_voice()"
            )
            return [{"error": str(error)}, 400]

class VoiceGeneratorV2(object):

    def __init__(self) -> None:

        self.success_logger = Logger(f"{CURRENT_PATH}/log/access.log")
        self.error_logger = Logger(f"{CURRENT_PATH}/log/errors.log")
        self.esng = Speaker()

    def _generate_voice(self, text: str, voice="ro") -> AudioSegment:
        import subprocess, tempfile
        with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
            subprocess.run([
                "espeak-ng",
                f"-v{voice}",
                "-w", tmp.name,
                text
            ], check=True)
            return AudioSegment.from_file(tmp.name, format="wav")

    def _generate_empty(self, duration: int) -> AudioSegment:
        """Generate silence (duration in seconds)."""
        return AudioSegment.silent(duration=duration * 1000)  # ms

    def _generate_sound(self, sound: str) -> AudioSegment:
        """Load a predefined sound effect by name."""
        try:
            # You can store your sound effects in a folder like ./sounds/
            sound_map = {
                "keyboard typing": "sounds/keyboard_typing.wav",
                "computer alerts": "sounds/computer_alert.wav",
                "whirring fans": "sounds/fans.wav",
                "bird": "sounds/bird.wav",
                "steps": "sounds/steps.wav"
            }
            if sound not in sound_map:
                raise ValueError(f"Sound effect '{sound}' not found in map")

            return AudioSegment.from_file(sound_map[sound], format="wav")
        except Exception as e:
            self.error_logger.create_error_log(
                f"Exception: {str(e)}. [object] VoiceGeneratorV2 [method] _generate_sound()"
            )
            return AudioSegment.silent(duration=1000)  # fallback

    def generate_voice(self, audio_script: list, voice: str = "ro") -> list:
        """
        Generate audio from script and return one concatenated audio file (bytes).
        """
        try:
            self.esng.voice = voice
            final_audio = AudioSegment.silent(duration=0)

            for part in audio_script:
                if part["type"] == "voice":
                    clip = self._generate_voice(part["text"])

                elif part["type"] == "empty":
                    clip = self._generate_empty(part["duration"])
                else:
                    clip = AudioSegment.silent(duration=0)  # fallback

                final_audio += clip  # concatenate

            # Export final audio
            output_buffer = io.BytesIO()
            final_audio.export(output_buffer, format="wav")
            output_buffer.seek(0)

            return [{"audio_object": output_buffer.read()}, 200]

        except Exception as error:
            self.error_logger.create_error_log(
                f"Exception: {str(error)}. [object] VoiceGeneratorV2 [method] generate_voice()"
            )
            return [{"error": str(error)}, 400]

s2  = [
  {
    "type": "empty",
    "duration": 2
  },
  {
    "type": "voice",
    "text": "In the shadows, hackers paint a digital canvas."
  },
  {
    "type": "voice",
    "text": "With every keystroke, they break barriers."
  },
  {
    "type": "voice",
    "text": "But remember, with power comes responsibility."
  },
  {
    "type": "empty",
    "duration": 2
  },
  {
    "type": "voice",
    "text": "Are you ready to join the ranks?"
  }
]
# with open(f'{CURRENT_PATH}\\output.mp3', 'wb') as f:
#
#     f.write(data)
#
#     f.close()