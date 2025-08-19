import requests, os
import platform

from utils.ai import GenerateShortScript
from dotenv import load_dotenv

CURRENT_PATH_FILE = os.path.abspath(__file__)
CURRENT_PATH = os.path.dirname(CURRENT_PATH_FILE)

slash = '\\'
OS = 'Windows'
if platform.system() == 'Linux':
    OS = 'Linux'
    slash = "/"  # path of the sql Queries folder
    load_dotenv(dotenv_path=f'{CURRENT_PATH}..{slash}.env')
else:
    load_dotenv(dotenv_path=f'{CURRENT_PATH}..{slash}.env')

API_IP = os.getenv("API")

print(API_IP)
class YoutubeBot(object):

    def __init__(self, channel_data : dict):

        self.channel_data = channel_data
        self.json_data = {}

        if 'category' in channel_data:
            self.json_data.update({'category' : channel_data['category'],})
            self.script_tool = GenerateShortScript(channel_data['category'])

    def get_video(self) -> dict:

        try:

            script = self.script_tool.generate_script()

            if 'error' in script:

                print("Error in script:",script['error'])

            elif 'script' in script:
                print("SCRIPT:", script['script'])
                self.json_data.update({'audio_script' : script['script']})

            res = requests.post(f'{API_IP}/get-random-video', json=self.json_data, stream=True)

            if res.status_code == 200:
                video_path = f"{CURRENT_PATH}{slash}received_video.mp4"
                with open(video_path, "wb") as f:
                    for chunk in res.iter_content(chunk_size=8192):
                        if chunk:  # ignore keep-alive chunks
                            f.write(chunk)
                    f.close()

                return {
                    'video-path' :  video_path
                }

            else:

                return {
                    'error': f"Exception: {res.status_code} - {res.text} [object] YoutubeBot [method] get_video()"
                }

        except Exception as error:

            return {
                'error' : f"Exception: {str(error)} [object] YoutubeBot [method] get_video()"
            }

YoutubeBot({'category' : 'hacking'}).run()