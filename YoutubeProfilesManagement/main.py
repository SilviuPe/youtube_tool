import  os
import platform
import json

from dotenv import load_dotenv
from log.logger import Logger
# from YoutubeBot.main import YoutubeBot

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


class YoutubeProfileManagement(object):

    def __init__(self) -> None:

        self.access_logger = Logger(path=f"{CURRENT_PATH}{slash}log{slash}access.log")
        self.errors_logger = Logger(path=f"{CURRENT_PATH}{slash}log{slash}errors.log")



        # Create an automation bot for each profile
        self.youtube_automation_bot_list = []

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

print(YoutubeProfileManagement().load_profiles_linking())