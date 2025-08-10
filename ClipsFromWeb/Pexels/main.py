import undetected_chromedriver as uc
import time
import os, sys
import base64
import requests

from .log.logger import Logger
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from Database.main import DatabaseConnection

CURRENT_PATH_FILE = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(CURRENT_PATH_FILE)

class PexelsScraper(object):

    """
    Object to scrape on pexels.com website
    """

    def __init__(self) -> None:

        self.driver = uc.Chrome(options = self.generate_options_for_chrome())

        self.success_logger = Logger(f"{CURRENT_DIR}\\log\\access.log")
        self.error_logger = Logger(f"{CURRENT_DIR}\\log\\errors.log")

        self.database = DatabaseConnection()

    @staticmethod
    def generate_options_for_chrome() -> Options:
        options = Options()
        # options.headless = True  # Run Chrome in headless mode (no GUI)
        options.add_argument("--window-size=1920,1080")  # Set window size (important for some sites)

        return options


    def download_video_from_url(self, video_url: str, output_name: str = 'video') -> str:

        if 'videos' not in os.listdir(CURRENT_DIR):
            self.error_logger.create_info_log("No 'videos' direcotry found to save videos. I'll create a new one. [object] PexelsScraper [method] download_video_from_url()")
            os.mkdir(f'{CURRENT_DIR}\\videos')

        if type(video_url) == str:

            filename = f"{output_name}.mp4"
            save_path = os.path.join(f'{CURRENT_DIR}\\videos\\', filename)

            try:
                # Download with streaming
                with requests.get(video_url, stream=True) as r:

                    r.raise_for_status()  # Raise error if download fails

                    with open(save_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)

                self.success_logger.create_success_log(f"Downloaded the video [{filename}] successfully. [object] PexelsScraper [method] download_video_from_url()")

                return save_path
            except Exception as error:
                self.error_logger.create_error_log(f"Exception: {str(error)}. [object] PexelsScraper [method] download_video_from_url()")

                return ''

        else:
            self.error_logger.create_error_log("A different type was provided instead of a link for the video or list with more links. "
                                               "[object] PexelsScraper [method] download_video_from_url()")

            return ''


    def __convert_into_base64url(self, path_of_video: str) -> str:
        """
        Private method to convert a .mp4 file into Base64 URL
        :param: path_of_video -> path of the .mp4 file. Absolute path recommended
        """
        try:

            with open(path_of_video, 'rb') as video_file:
                video_bytes = video_file.read()
            base64url_str = base64.urlsafe_b64encode(video_bytes).decode('utf-8')

            return base64url_str

        except Exception as error:
            self.error_logger.create_error_log(f"Exception: {str(error)} [object] PexelsScraper [method] convert_into_base64url()")

            return ''


    def get_new_videos(self, keyword: str = "", videos_qt: int = 0) -> list:
        """
        Method to get new videos from pexels.com
        :param: keyword - keywords search
        """
        try:
            self.driver.get(f"https://www.pexels.com/search/videos/{keyword}/")

            time.sleep(3)  # wait for page to load

            self.success_logger.create_info_log("Successfully loaded the page www.pexels.com . [object] PexelsScraper [method] get_new_videos()")

            results = []

            try:
                containers = self.driver.find_elements(By.CSS_SELECTOR, 'div.BreakpointGrid_item__RSMyf')

                if not videos_qt or videos_qt > len(containers):
                    videos_qt = len(containers)

                for index in range(videos_qt):
                    # 1️⃣ Get video page link (first <a>)
                    container = containers[index]
                    try:
                        a_tag = container.find_element(By.TAG_NAME, 'a')
                        page_href = a_tag.get_attribute("href")
                        if page_href and page_href.startswith("/"):
                            page_href = f"https://www.pexels.com{page_href}"

                    except Exception as error:
                        self.error_logger.create_error_log(f"Exception: {str(error)}. [object] PexelsScraper [method] get_new_videos()")
                        continue

                    # 2️⃣ Get download link
                    try:
                        download_a = container.find_element(By.CSS_SELECTOR, 'a.DownloadButton_downloadButton__0aNOo')
                        download_href = download_a.get_attribute("href")

                    except Exception as error:
                        self.error_logger.create_error_log(f"Exception: {str(error)}. [object] PexelsScraper [method] get_new_videos()")
                        continue

                    # Check if the video already exists in database
                    if len(self.database.request_pexels_video(id_ = True, conditions={"download_link" : download_href,
                                                                                      "video_link" : page_href,
                                                                                      "key_word_search" : keyword})):
                        continue

                    video_name = page_href.split('/')[-2]
                    path = self.download_video_from_url(video_url=download_href, output_name=video_name)

                    if len(path):

                        base64_string = self.__convert_into_base64url(path)

                        results.append({
                            "video_link": page_href,
                            "download_link": download_href,
                            "base64_string": base64_string,
                            "key_word_search": keyword,
                            "base64_length": len(base64_string)
                        })

                    else:
                        self.error_logger.create_error_log(f"Exception trying to convert file to base64. [object] PexelsScraper [method] get_new_videos()")


            except Exception as error:
                self.error_logger.create_error_log(
                    f"Exception: {str(error)} [object] PexelsScraper [method] get_video_page_and_download_links()"
                )

            return results


        except Exception as error:
            self.error_logger.create_error_log(f"Exception: {str(error)} [object] PexelsScraper [method] get_new_videos()")

            return []
