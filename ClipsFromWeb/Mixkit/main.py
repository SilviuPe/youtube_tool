import keyword
import os
import requests

from bs4 import BeautifulSoup

from .log.logger import Logger

from Database.main import DatabaseConnection

CURRENT_PATH_FILE = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(CURRENT_PATH_FILE)




class MixkitScraper(object):

    """
    Object to scrape on mixkit.com website
    """

    def __init__(self) -> None:

        self.driver = None

        self.success_logger = Logger(f"{CURRENT_DIR}\\log\\access.log")
        self.error_logger = Logger(f"{CURRENT_DIR}\\log\\errors.log")

        self.database = DatabaseConnection()


    def get_new_videos(self, keyword: str = "", videos_qt: int = 0) -> list:
        """
        Method to get new videos from mixkit.co
        :param: keyword - keywords search
        """

        link = f"https://mixkit.co/free-stock-video/discover/{keyword}/?orientation=vertical"

        try:

            response = requests.get(link)

            if response.status_code != 200:

                self.error_logger.create_error_log("Error getting a 200 status code from mixkit.co . Please check. [object] MixkitScraper [method] get_new_videos()")

                return []

            else:

                html_content = response.content.decode()
                results = []

                if html_content:

                    soup = BeautifulSoup(html_content, "html.parser")

                    videos = soup.find_all("video")
                    h2 = soup.find_all("h2", class_="item-grid-card__title")

                    if not len(videos):

                        self.error_logger.create_error_log(
                            "No videos were found. Please check. [object] MixkitScraper [method] get_new_videos()")

                        return []

                    """
                    results.append({
                        "video_link": page_href,
                        "download_link": download_href,
                        "key_word_search": keyword,
                        "save_data" : {
                            "filename" : file_name
                        }
                    })
                    """

                    for index in range(len(videos)):

                        download_link = ''
                        video_link = ''

                        if videos[index].get("src", "").endswith(".mp4"):
                            download_link = videos[index]["src"]

                        a_tag = h2[index].find("a")

                        if a_tag:
                            video_link = a_tag.get("href")

                            if video_link.startswith('/'):
                                video_link = "www.mixkit.co" + video_link

                        results.append({
                            "video_link": video_link,
                            "download_link": download_link,
                            "key_word_search": keyword,
                            "save_data": {
                                "filename": video_link.split("/")[-2],
                            }
                        })

                return results

        except Exception as error:

            self.error_logger.create_error_log(f"Exception: {str(error)}. [object] MixkitScraper [method] get_new_videos()")

            return []


# videos_data = MixkitScraper().get_new_videos(keyword="hacking")
#
# print(videos_data)
# print(videos_data)


