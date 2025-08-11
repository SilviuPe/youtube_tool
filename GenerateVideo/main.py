import os
import json
import requests
import platform

from dotenv import load_dotenv

from GenerateVoice.main import AIGenerateVoice
from Database.main import DatabaseConnection

from .log.logger import Logger
from .utils.audio import get_media_duration, write_bytes_to_file

CURRENT_PATH_FILE = os.path.abspath(__file__)
CURRENT_PATH = os.path.dirname(CURRENT_PATH_FILE)

# slash

slash = '\\'
if platform.system() == 'Linux':
    slash = "/"  # path of the sql Queries folder

load_dotenv(dotenv_path=f'{CURRENT_PATH}..{slash}.env')

"""

DOCUMENTATION:

This VideoGenerator uses Heygen API:
    
    - Website: https://heygen.com
    - API Documentation: https://docs.heygen.com/docs/create-video
    
    
"""
API_DATA = {
            "avatars" : {
                "path": "https://api.heygen.com/v2/avatars",
                "method": "GET"
            },
            "voices" : {
                "path" : "https://api.heygen.com/v2/voices",
                "method": "GET"
            },
            "generate_video" : {
                "path" : "https://api.heygen.com/v2/video/generate",
                "method": "POST"
            }
        }
API_IP = os.getenv("API")

class AIVideoGenerator(object):

    def __init__(self, api_key) -> None:

        self.api_key = api_key

        self.success_logger = Logger(f"{CURRENT_PATH}\\log\\access.log")
        self.error_logger = Logger(f"{CURRENT_PATH}\\log\\errors.log")


    def generate_data(self) -> None:

        pass


    def generate_video(self) -> list:

        pass

    def list_voices(self) -> list:
        """
        Method to list all available voices.
        API URL: https://api.heygen.com/v2/voices
        """
        try:
            api = API_DATA['voices']
            api_response = requests.request(
                method=api['method'],
                url=api['path'],
                headers={
                    'Content-Type': 'application/json',
                    'x-api-key': self.api_key
                })

            response_content: dict = json.loads(api_response.content.decode('utf-8'))

            if api_response.status_code == 401:
                self.error_logger.create_error_log(
                    f"Error occurred: {response_content['error']['message']} [object] VideoGenerator [method] list_voices()")
                return [{"error": response_content['error']['message']}, 400]

            if api_response.status_code == 200:
                if 'data' in response_content and 'voices' in response_content['data']:
                    return [response_content['data']['voices'], 200]
                else:
                    self.error_logger.create_error_log(
                        "Invalid response format [object] VideoGenerator [method] list_voices()")
                    return [{"error": "Invalid response format"}, 400]

            self.error_logger.create_error_log(
                f"Unexpected status: {api_response.status_code} [object] VideoGenerator [method] list_voices()")
            return [{"error": f"Unexpected status: {api_response.status_code}"}, 400]

        except Exception as error:
            self.error_logger.create_error_log(
                f"Exception: {str(error)} [object] VideoGenerator [method] list_voices()")
            return [{"error": str(error)}, 400]



    def list_avatars(self) -> list:

        """

        Method to list all available avatars

        API URL: https://api.heygen.com/v2/avatars
        API Documentation for avatars: https://docs.heygen.com/reference/list-voices-v2
        """

        try:

            # get the api data for list of avatars

            api = API_DATA['avatars']


            # create the request using the API data
            api_response = requests.request(method=api['method'], url=api['path'], headers = {
                'Content-Type' : 'application/json',
                'x-api-key' : self.api_key
            })

            # get the content from the response
            response_content: dict = json.loads(api_response.content.decode('utf-8'))


            """
                Check the status code:
                    
                    200 - Everything worked well, no issues found
                    401 - Maybe the API KEY is wrong but usually means unauthorized
                    
                    Check API documentation for further information
                    
            """

            if api_response.status_code == 401:

                self.error_logger.create_error_log(f"Error occurred: {response_content['error']['message']} [object] VideoGenerator [method] list_avatars()")

                return [ {"error": response_content['error']['message']}, 400 ]

            if api_response.status_code == 200:

                if 'data' in response_content:

                    if 'avatars' in response_content['data']:
                        return [ response_content['data']['avatars'] , 200 ]
                    else:
                        self.error_logger.create_error_log("Error occurred while trying to get the 'voices' from response content. [object] VideoGenerator [method] list_avatars()")

                        return [{"error" : "Error occurred while trying to get the 'voices' from response content. [object] VideoGenerator [method] list_avatars()"}, 400]
                else:
                    self.error_logger.create_error_log(
                        "Error occurred while trying to get the 'data' from response content. [object] VideoGenerator [method] list_avatars()")

                    return [{
                                "error": "Error occurred while trying to get the 'data' from response content. [object] VideoGenerator [method] list_avatars()"}, 400]
            else:

                self.error_logger.create_error_log(f"Unexpected error occurred. Status 200 expected but got {api_response.status_code}. Check API Documentation or enable Debug mode. [object] VideoGenerator [method] list_avatars()")

                return [{ "error" : f"Unexpected error occurred. Status 200 expected but got {api_response.status_code}. Check API Documentation or enable Debug mode. [object] VideoGenerator [method] list_avatars()"}, 400]

        except Exception as error:

            self.error_logger.create_error_log(f"Error occured: {str(error)} [object] VideoGenerator [method] list_avatars()")

            return [ {"error" : str(error)}, 400 ]


class ManualVideoGenerator(object):

    """
    Object to generate videos from scratch
    """

    def __init__(self, average_video_seconds: int = 4) -> None:
        self.average_video_seconds = average_video_seconds

        self.voice_tool = AIGenerateVoice(api_key=os.getenv("ELEVENLABS_API_KEY"), voice_id="29vD33N1CtxCmqQRPOHJ")
        self.db_connection = DatabaseConnection()

    def generate_audio(self, speech: str, download: bool = False) -> bytes:
        """
        Method to generate the audio from text using AI
        """
        voice_gen = self.voice_tool.generate_voice(speech)[0]['audio_object']  # generator

        # Collect all chunks from generator into a single bytes object
        audio_bytes = b"".join(chunk for chunk in voice_gen)

        if download:
            self.voice_tool.write_out_voice(audio_bytes, output_path=f"{CURRENT_PATH}\\output.mp3")

        return audio_bytes

    def define_videos_data(self, duration : int):

        videos_qt = int(duration/self.average_video_seconds)
        last_video_duration = self.average_video_seconds + (duration % self.average_video_seconds)

        data = {
            "video_qt" : videos_qt,
            "last_video_duration" : last_video_duration
        }

    def generate_video(self) -> None:

        audio_bytes = self.generate_audio(
            "Hackers don’t knock. They move silently, slipping through the cracks you never see. Every click, every open network — an open door. By the time you notice, they’re already inside, taking what’s yours. Stay protected… before it’s too late.")

        write_bytes_to_file(audio_bytes, f"{CURRENT_PATH}{slash}audio.mp3")
        audio_duration = get_media_duration(audio_bytes)

        print(audio_duration)

ManualVideoGenerator().generate_video()