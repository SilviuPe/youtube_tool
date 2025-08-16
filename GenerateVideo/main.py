import os
import json
import requests
import platform
import subprocess
import tempfile
import whisper

from dotenv import load_dotenv

from GenerateVoice.main import AIGenerateVoice
from Database.main import DatabaseConnection

from .log.logger import Logger
from .utils.audio import get_media_duration, write_bytes_to_file

CURRENT_PATH_FILE = os.path.abspath(__file__)
CURRENT_PATH = os.path.dirname(CURRENT_PATH_FILE)

# slash

slash = '\\'
OS = 'Windows'
if platform.system() == 'Linux':
    OS = 'Linux'
    slash = "/"  # path of the sql Queries folder
else:
    load_dotenv(dotenv_path=f'{CURRENT_PATH}..{slash}.env')
    API_IP = os.getenv("API")

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


def sec_to_ass_time(sec):
    """Convertește secunde în format ASS h:mm:ss.cs"""
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int((sec % 1) * 100)  # centisecunde
    return f"{h}:{m:02}:{s:02}.{cs:02}"


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

    def define_video_data(self, audio_script : str):

        audio_bytes = self.generate_audio(audio_script)
        audio_duration = get_media_duration(audio_bytes)

        videos_qt = int(audio_duration/self.average_video_seconds)
        last_video_duration = self.average_video_seconds + (audio_duration % self.average_video_seconds)

        data = {
            "video_qt" : videos_qt,
            "last_video_duration" : last_video_duration,
            "audio_bytes": audio_bytes
        }

        return data

    def generate_video(self, video_paths: list, audio_bytes: bytes, last_video_duration: float) -> bytes:

        # === PATH FFmpeg ===

        ffmpeg_path = ''
        if OS == 'Windows':
            ffmpeg_path = os.path.join(CURRENT_PATH, "ffmpeg", "bin", "ffmpeg.exe")
        if OS == 'Linux':
            ffmpeg_path = 'ffmpeg'

        temp_dir = tempfile.mkdtemp()
        processed_videos = []

        # === 1. Prelucrează fiecare video cu fade in/out ===
        for i, path in enumerate(video_paths):
            target_duration = last_video_duration if i == len(video_paths) - 1 else self.average_video_seconds
            output_path = os.path.join(temp_dir, f"clip_{i}.mp4")
            processed_videos.append(output_path)

            fade_in = 0.5
            fade_out = 0.5

            cmd = (
                f'"{ffmpeg_path}" -y -i "{path}" '
                f'-t {target_duration} '
                f'-vf "fade=t=in:st=0:d={fade_in},fade=t=out:st={target_duration - fade_out}:d={fade_out}" '
                f'"{output_path}"'
            )
            subprocess.run(cmd, shell=True, check=True)

        # === 2. Concatenează videoclipurile ===
        concat_file = os.path.join(temp_dir, "concat_list.txt")
        with open(concat_file, "w", encoding="utf-8") as f:
            for clip in processed_videos:
                f.write(f"file '{clip}'\n")

        temp_audio_path = os.path.join(temp_dir, "audio.mp3")
        with open(temp_audio_path, "wb") as f:
            f.write(audio_bytes)

        concat_output = os.path.join(temp_dir, "concatenated.mp4")
        cmd_concat = f'"{ffmpeg_path}" -y -f concat -safe 0 -i "{concat_file}" -c copy "{concat_output}"'
        subprocess.run(cmd_concat, shell=True, check=True)

        # === 3. Adaugă audio-ul final ===
        video_with_audio = os.path.join(temp_dir, "with_audio.mp4")
        cmd_final = (
            f'"{ffmpeg_path}" -y -i "{concat_output}" -i "{temp_audio_path}" '
            f'-c:v copy -c:a aac -map 0:v:0 -map 1:a:0 "{video_with_audio}"'
        )
        subprocess.run(cmd_final, shell=True, check=True)

        # === 4. Rulează Whisper pentru subtitrări ===
        model = whisper.load_model("small")  # sau "large" pt. acuratețe maximă
        result = model.transcribe(video_with_audio, word_timestamps=True)

        # === 5. Creează fișier ASS cu styling TikTok ===
        subs_path = os.path.join(temp_dir, "subs.ass")
        with open(subs_path, "w", encoding="utf-8") as f:
            f.write("""[Script Info]
            ScriptType: v4.00+
            PlayResX: 1080
            PlayResY: 1920
            Collisions: Normal
            WrapStyle: 2
            ScaledBorderAndShadow: yes
        
            [V4+ Styles]
            Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
            Style: TikTok,Impact,64,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,4,2,2,20,20,100,0
        
            [Events]
            Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
            """)

            sub_id = 1
            for seg in result["segments"]:
                words = seg["words"]
                for i in range(0, len(words), 3):  # grupuri de 3 cuvinte
                    chunk = words[i:i + 3]
                    if not chunk:
                        continue
                    start = chunk[0]["start"]
                    end = chunk[-1]["end"]
                    text = " ".join([w["word"].strip() for w in chunk])

                    f.write(f"Dialogue: 0,{sec_to_ass_time(start)},{sec_to_ass_time(end)},TikTok,,0,0,0,,{text}\n")
                    sub_id += 1

        # === 6. Aplică subtitrările pe video final ===
        output_path = os.path.join(temp_dir, "output.mp4")
        cmd_subs = (
            f'"{ffmpeg_path}" -y -i "{video_with_audio}" '
            f'-vf "scale=-1:1920,crop=1080:1920,ass={subs_path}" '
            f'-c:a copy "{output_path}"'
        )
        subprocess.run(cmd_subs, shell=True, check=True)

        # === 7. Întoarce video-ul final în bytes ===
        with open(output_path, "rb") as f:
            video_bytes = f.read()

        # Curățare fișiere temporare
        try:
            for file in processed_videos:
                os.remove(file)
            os.remove(concat_file)
            os.remove(temp_audio_path)
            os.remove(concat_output)
            os.remove(video_with_audio)
            os.remove(subs_path)
            os.remove(output_path)
            os.rmdir(temp_dir)
        except Exception:
            pass

        return video_bytes