import undetected_chromedriver as uc
import time
import os
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
        # options.add_argument("--window-size=1920,1080")  # Set window size (important for some sites)

        # options.add_argument("--headless=new")  # new headless mode in Chrome
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
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

                    file_name = page_href.split('/')[-2]

                    results.append({
                        "video_link": page_href,
                        "download_link": download_href,
                        "key_word_search": keyword,
                        "save_data" : {
                            "filename" : file_name
                        }
                    })

            except Exception as error:
                self.error_logger.create_error_log(
                    f"Exception: {str(error)} [object] PexelsScraper [method] get_video_page_and_download_links()"
                )

            return results


        except Exception as error:
            self.error_logger.create_error_log(f"Exception: {str(error)} [object] PexelsScraper [method] get_new_videos()")

            return []


tool = PexelsScraper()
videos = tool.get_new_videos("car", 5)
print(videos)

req = requests.post("http://109.176.199.63:5000/save_new_data", json=videos)
print(req.content)