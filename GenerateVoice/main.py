from elevenlabs.client import ElevenLabs
from GenerateVoice.log.logger import Logger
import os

CURRENT_PATH_FILE = os.path.abspath(__file__)

"""

DOCUMENTATION:

This VoiceGenerator uses Elevenlabs API:
Website: https://elevenlabs.io/

API Documentation: https://elevenlabs.io/docs/api-reference/introduction

You do not have a way to check if the API is still valid, you'll gen an answer from the genetate_voice() function to check if is not available anymore.
"""


class VoiceGenerator(object):
    
    """
    Class to generate voices from text 
    """

    def __init__(self, api_key: str, voice_id: str, model_id: str) -> None:
        
        self.lab = ElevenLabs(api_key)
        self.voice_id = voice_id
        self.model_id = model_id

        self.success_logger = Logger(f"{CURRENT_PATH_FILE}/log/access.log")
        self.error_logger = Logger(f"{CURRENT_PATH_FILE}/log/errors.log")


    def genetate_voice(self, text :  str) -> list:

        """
        
        Method to generate the voice from text
        
        :param: text - the script for the voice

        """

        try:
            
            audio_stream = self.lab.text_to_speech.stream(
                text=text,
                voice_id=self.voice_id,
                model_id=self.model_id
            )

            self.success_logger.create_success_log("Audio voice succesfully created. [object] GenerateVoice [method] generate_voice()")

            return [{"audio_object" : audio_stream
            }, 200]


        except Exception as error:
            
            self.error_logger.create_error_log(f"Error occurred: {str(error)}. [object] GenerateVoice [method] generate_voice()")

            return [{"error" : str(error)
            } , 400]



    def write_out_voice(self, binary_content : bytes) -> list:
        """
        
        Method to write out an .mp3 file

        """

        try:

            with open("output.mp3", "wb") as f:
                
                for binary_data in binary_content:
                    if isinstance(binary_data, bytes):
                        f.write(binary_data)

                f.close()

            self.success_logger.create_success_log("Audio voice file succesfully created. [object] GenerateVoice [method] write_out_voice()")

            return [{}, 200]

        except Exception as error:

            self.error_logger.create_error_log(f"Error occurred: {str(error)}. [object] GenerateVoice [method] write_out_voice()")

            return [{"error" : str(error)
            } , 400]