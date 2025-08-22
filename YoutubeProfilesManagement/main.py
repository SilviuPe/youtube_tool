import  os
import platform
import json
import time
import requests

from dotenv import load_dotenv
from .log.logger import Logger
from YoutubeBot.main import YoutubeBot

CURRENT_PATH_FILE = os.path.abspath(__file__)
CURRENT_PATH = os.path.dirname(CURRENT_PATH_FILE)

slash = '\\'

if platform.system() == 'Linux':
    slash = "/"  # path of the sql Queries folder

load_dotenv(dotenv_path=f'{CURRENT_PATH}{slash}..{slash}.env')
API_IP = os.getenv("API")

print(f'{CURRENT_PATH}..{slash}.env')

class YoutubeProfileManagement(object):

    def __init__(self) -> None:

        self.access_logger = Logger(path=f"{CURRENT_PATH}{slash}log{slash}access.log")
        self.errors_logger = Logger(path=f"{CURRENT_PATH}{slash}log{slash}errors.log")

        self.timer_to_post = 60*60*4 # hours

        # Create an automation bot for each profile
        self.youtube_automation_bot_list = []
        self.script_running = True

        self.profile_linking = self.load_profiles_linking()
        self.file_profiles = self.load_all_profiles()


    def load_all_profiles(self) -> list:

        try:

            if "profiles" in os.listdir(CURRENT_PATH):

                all_profiles = os.listdir(rf"{CURRENT_PATH}{slash}profiles")
                profiles = []
                for profile in all_profiles:
                    path = rf"{CURRENT_PATH}{slash}profiles{slash}{profile}"
                    if os.path.isdir(path):
                        self.access_logger.create_info_log(f"Found profile: \"{profile}\"")
                        profiles.append(path)

                return profiles

            else:
                self.access_logger.create_warning_log(
                    f"No \"profiles\" folder found. [object] YoutubeProfileManagement [method] load_all_profiles()")

                os.mkdir(f"{CURRENT_PATH}{slash}profiles")

                self.access_logger.create_info_log(
                    f"New \"profiles\" created in {CURRENT_PATH}. [object] YoutubeProfileManagement [method] load_all_profiles()")

                return self.load_all_profiles()

        except Exception as error:

            self.errors_logger.create_error_log(f"Exception: {str(error)} [object] YoutubeProfileManagement [method] load_all_profiles()")

            return []

    def load_profiles_linking(self) -> dict:

        try:

            if "profiles_linking.json" in os.listdir(fr"{CURRENT_PATH}{slash}profiles"):

                with open(rf"{CURRENT_PATH}{slash}profiles{slash}profiles_linking.json") as json_file:

                    json_content = json.loads(json_file.read())
                    json_file.close()

                    self.access_logger.create_info_log(
                        f"Found linking file in {CURRENT_PATH}{slash}profiles. [object] YoutubeProfileManagement [method] load_all_profiles()")

                    return json_content

            else:

                self.access_logger.create_warning_log(
                    f"Cannot find linking file in {CURRENT_PATH}{slash}profiles. [object] YoutubeProfileManagement [method] load_all_profiles()")

                # Write it to the file
                with open(fr"{CURRENT_PATH}{slash}profiles{slash}profiles_linking.json", "w") as f:
                    json.dump({}, f)

                self.access_logger.create_info_log(
                    "Linking file created successfully. [object] YoutubeProfileManagement [method] load_all_profiles()"
                )

                return {}

        except Exception as error:

            self.errors_logger.create_error_log(
                f"Exception: {str(error)} [object] YoutubeProfileManagement [method] load_profiles_linking()")

            return {
                "error" : f"{str(error)}",
            }


    def get_all_channels(self) -> list:

        end_point = '/channels'

        try:
            response = requests.get(API_IP+end_point)

            content = response.content.decode()

            conversion_content_to_list = json.loads(content)

            return conversion_content_to_list

        except Exception as error:

            self.errors_logger.create_error_log(
                f"Exception: {str(error)} [object] YoutubeProfileManagement [method] get_all_channels()")

            return []


    def run(self) -> None:

        get_video_end_point = '/get_random_video'

        try:
            channels = self.get_all_channels()

            if channels:

                while self.script_running:

                    for channel_data in channels:

                        if not "channel_id" in channel_data:

                            self.errors_logger.create_error_log(
                                "A channel misses the \"channel_id\" key. Please, check the DATABASE!"
                            )
                            continue

                        if not 'nickname' in channel_data:

                            self.errors_logger.create_warning_log(
                                f"Channel with ID: \"{channel_data['channel_id']}\" do not have a nickname assigned. Please, check the DATABASE!"
                            )
                            continue

                        if not 'category' in channel_data:

                            self.errors_logger.create_warning_log(
                                f"Channel with ID: \"{channel_data['channel_id']}\" do not have a category assigned. Please, check the DATABASE!"
                            )
                            continue

                        youtube_bot = YoutubeBot(channel_data)

                        profile_path = ''

                        for profile in self.file_profiles:

                            if channel_data['nickname'] in profile:
                                profile_path = profile


                        youtube_bot.post_on_youtube(profile_path, channel_data['video_style_id'])

                        del youtube_bot

                    return

            else:

                self.errors_logger.create_warning_log(
                    f"No channels were found in the database, manual checking might be required. [object] YoutubeProfileManagement [method] run()")

                return


        except Exception as error:

            self.errors_logger.create_error_log(
                f"Exception: {str(error)} [object] YoutubeProfileManagement [method] get_all_channels()")

YoutubeProfileManagement().run()