from elevenlabs.client import ElevenLabs
from .log.logger import Logger
from dotenv import load_dotenv

import os
import json
import requests

import pyttsx3
import tempfile


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

    def generate_voice(self, text: str, voice: str = "ro-RO-EmilNeural") -> list:
        """
        Generează audio din text și returnează datele audio în format bytes.

        Args:
            text (str): Textul de convertit în vorbire.
            voice (str): Numele vocii utilizate pentru sinteză.

        Returns:
            bytes: Datele audio generate.
        """
        try:
            # Inițializare engine pyttsx3
            engine = pyttsx3.init()

            # Setare voce
            voices = engine.getProperty('voices')
            for v in voices:
                if voice in v.id:
                    engine.setProperty('voice', v.id)
                    break

            # Creare fișier temporar pentru audio
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_file_path = temp_file.name

            # Salvare audio în fișier
            engine.save_to_file(text, temp_file_path)
            engine.runAndWait()

            del engine

            # Citire conținut fișier audio
            with open(temp_file_path, 'rb') as audio_file:
                audio_data = audio_file.read()

            # Ștergere fișier temporar
            os.remove(temp_file_path)

            return [{"audio_object": audio_data}, 200]

        except Exception as error:
            self.error_logger.create_error_log(
                f"Exception: {str(error)}. [object] ManualGenerateVoice [method] generate_voice()"
            )

            return [{"error": str(error)}, 400]

# tool = GenerateVoice(api_key=os.getenv("ELEVENLABS_API_KEY"), voice_id="29vD33N1CtxCmqQRPOHJ")
# voices = tool.get_all_voices()

# for voice in voices['voices']:
#     print(voice['name'], voice['voice_id'])
#     print()
# voice = tool.generate_voice("Hello everyone! Did you hear about this new feature from Facebook?")[0]['audio_object']
#
# tool.write_out_voice(voice)