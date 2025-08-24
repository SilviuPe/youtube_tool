import time

from ClipsFromWeb.Pexels.main import PexelsScraper
from ClipsFromWeb.Mixkit.main import MixkitScraper

from Database.main import DatabaseConnection

from .log.logger import Logger

from dotenv import load_dotenv

import os
import platform
import requests
import ssl
import certifi

# Fix SSL issues
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())

CURRENT_PATH_FILE = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(CURRENT_PATH_FILE)

slash = '\\'
if platform.system() == 'Linux':
    slash = "/"  # path of the sql Queries folder

load_dotenv(dotenv_path=f'{CURRENT_PATH_FILE}{slash}..{slash}.env')

API_IP = os.getenv('API')
END_POINT = '/save-new-data'



class PexelsMonitor(object):

    def __init__(self) -> None:

        self.success_logger = Logger(f"{CURRENT_DIR}{slash}log{slash}access.log")
        self.error_logger = Logger(f"{CURRENT_DIR}{slash}log{slash}errors.log")

        self.running_script = True

        self.time_before_next_scrape = 60*60*12

    def get_categories(self):

        try:

            db = DatabaseConnection()
            channels = db.get_channels()

            if not channels:
                self.error_logger.create_error_log(f"No channels found. [object] PexelsMonitor [method] get_categories()")

            return [channel['category'] for channel in channels]

        except Exception as error:

            self.error_logger.create_error_log(f"Exception: {str(error)} [object] PexelsMonitor [method] get_categories()")

    def request_for_new_videos(self, json_videos_data: list) -> None:

        try:

            response = requests.post(API_IP + END_POINT, json=json_videos_data)

            if response.status_code != 200:
                self.error_logger.create_warning_log(
                    f"Request to save new videos ({END_POINT}) returned status: {response.status_code}. Manual checking might be required.  PexelsMonitor [method] request_for_new_videos()")

        except Exception as error:
            self.error_logger.create_error_log(f"Exception: {str(error)} [object] PexelsMonitor [method] request_for_new_videos()")

    def run(self) -> None:

        try:

            while self.running_script:

                categories = self.get_categories()

                for category in categories:

                    scraper_tool = PexelsScraper()
                    videos = scraper_tool.get_new_videos(category)

                    self.request_for_new_videos(videos)

                    del scraper_tool

                time.sleep(self.time_before_next_scrape)

        except Exception as error:
            self.error_logger.create_error_log(f"Exception: {str(error)} [object] PexelsMonitor [method] run()")


class MixkitMonitor(object):

    def __init__(self) -> None:
        self.success_logger = Logger(f"{CURRENT_DIR}{slash}log{slash}access.log")
        self.error_logger = Logger(f"{CURRENT_DIR}{slash}log{slash}errors.log")

        self.running_script = True

        self.time_before_next_scrape = 60*60*12

    def get_categories(self):

        try:

            db = DatabaseConnection()
            channels = db.get_channels()

            if not channels:
                self.error_logger.create_error_log(f"No channels found. [object] PexelsMonitor [method] get_categories()")

            return [channel['category'] for channel in channels]

        except Exception as error:

            self.error_logger.create_error_log(f"Exception: {str(error)} [object] PexelsMonitor [method] get_categories()")

    def request_for_new_videos(self, json_videos_data: list) -> None:

        try:

            response = requests.post(API_IP + END_POINT, json=json_videos_data)

            if response.status_code != 200:
                self.error_logger.create_warning_log(
                    f"Request to save new videos ({END_POINT}) returned status: {response.status_code}. Manual checking might be required.  PexelsMonitor [method] request_for_new_videos()")

        except Exception as error:
            self.error_logger.create_error_log(f"Exception: {str(error)} [object] PexelsMonitor [method] request_for_new_videos()")

    def run(self) -> None:

        try:

            while self.running_script:

                categories = self.get_categories()

                for category in categories:

                    scraper_tool = MixkitScraper()
                    videos = scraper_tool.get_new_videos(category)

                    self.request_for_new_videos(videos)

                    del scraper_tool

                time.sleep(self.time_before_next_scrape)

        except Exception as error:
            self.error_logger.create_error_log(f"Exception: {str(error)} [object] PexelsMonitor [method] run()")


