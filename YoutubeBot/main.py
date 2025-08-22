import time

import requests, os
import platform
import undetected_chromedriver as uc



from dotenv import load_dotenv
from numba.scripts.generate_lower_listing import description
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from .utils.ai import GenerateShortScript
from .log.logger import Logger

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

        self.access_logger = Logger(path=f"{CURRENT_PATH}{slash}log{slash}access.log")
        self.errors_logger = Logger(path=f"{CURRENT_PATH}{slash}log{slash}errors.log")

        if 'category' in channel_data:
            self.json_data.update({'category' : channel_data['category']})
            self.script_tool = GenerateShortScript(channel_data['category'])

    def get_video(self, style_id: int) -> dict:

        try:

            script = self.script_tool.generate_script()

            if 'error' in script:

                print("Error in script:",script['error'])

            elif 'script' in script:
                print("SCRIPT:", script['script'])
                self.json_data.update({'audio_script' : script['script'], 'video_style_id' : style_id})

            res = requests.post(f'{API_IP}/get-random-video', json=self.json_data, stream=True)

            if res.status_code == 200:
                video_path = f"{CURRENT_PATH}{slash}received_video.mp4"
                with open(video_path, "wb") as f:
                    for chunk in res.iter_content(chunk_size=8192):
                        if chunk:  # ignore keep-alive chunks
                            f.write(chunk)
                    f.close()

                self.access_logger.create_success_log("Video created successfully!")

                return {
                    'video-path' :  video_path,
                    'title': script['title'],
                    'description': script['description'],
                }

            else:
                self.errors_logger.create_error_log(f"Exception: {res.status_code} - {res.text} [object] YoutubeBot [method] get_video()")
                return {
                    'error': f"Exception: {res.status_code} - {res.text} [object] YoutubeBot [method] get_video()",
                    'status_code' : 400
                }

        except Exception as error:
            self.errors_logger.create_error_log(
                 f"Exception: {str(error)} [object] YoutubeBot [method] get_video()")

            return {
                'error' : f"Exception: {str(error)} [object] YoutubeBot [method] get_video()",
                'status_code': 400
            }

    def __click_on_dropdown(self, driver: uc.Chrome) -> None:

        try:
            # Wait until the button is clickable
            wait = WebDriverWait(driver, 20)
            dropdown_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='Create']/ancestor::button"))
            )

            # Click the button
            dropdown_button.click()

            self.access_logger.create_info_log("Dropdown opened. [object] YoutubeBot [method] __click_on_dropdown()")

        except Exception as error:

            self.errors_logger.create_error_log(
                f"Exception: {str(error)} [object] YoutubeBot [method] __click_on_dropdown()")

    def __click_on_upload_button(self, driver: uc.Chrome) -> None:

        try:
            # Wait until the button is clickable
            wait = WebDriverWait(driver, 20)

            # Wait for the "Upload videos" menu item to appear
            upload_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//yt-formatted-string[text()='Upload videos']/ancestor::tp-yt-paper-item")
                )
            )

            # Click it
            upload_button.click()

            self.access_logger.create_info_log("Upload button pressed. [object] YoutubeBot [method] __click_on_upload_button()")

        except Exception as error:

            self.errors_logger.create_error_log(
                f"Exception: {str(error)} [object] YoutubeBot [method] __click_on_upload_button()")

    def __send_video(self, driver: uc.Chrome, file_path: str):
        try:
            # Wait until the button is clickable
            wait = WebDriverWait(driver, 20)

            # Wait for the file input element to be present
            file_input = wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )

            file_input.send_keys(file_path)

            self.access_logger.create_success_log("Video successfully uploaded. [object] YoutubeBot [method] __send_video()")

        except Exception as error:

            self.errors_logger.create_error_log(
                f"Exception: {str(error)} [object] YoutubeBot [method] __send_video()")

    def __type_in_title_textarea(self, driver: uc.Chrome, text: str) -> None:

        try:
            # Wait until the button is clickable
            wait = WebDriverWait(driver, 20)

            title_box = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#textbox[contenteditable='true']"))
            )

            # Click to focus
            title_box.click()

            # Optional: clear existing text
            title_box.send_keys(Keys.CONTROL + "a")
            title_box.send_keys(Keys.BACKSPACE)

            # Type your new title
            title_box.send_keys(text)

            self.access_logger.create_success_log("Text injected successfully in title textarea. [object] YoutubeBot [method] __type_in_title_textarea()")

        except Exception as error:

            self.errors_logger.create_error_log(
                f"Exception: {str(error)} [object] YoutubeBot [method] __type_in_title_textarea()")

    def __type_in_description_textarea(self,driver: uc.Chrome, text: str) -> None:

        try:
            # Wait until the button is clickable
            wait = WebDriverWait(driver, 20)

            # Wait until the description box is clickable
            description_box = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#textbox[aria-label^='Tell viewers about']"))
            )

            # Click to focus
            description_box.click()

            # Optional: clear existing text
            description_box.send_keys(Keys.CONTROL + "a")
            description_box.send_keys(Keys.BACKSPACE)

            # Type your new description
            description_box.send_keys(text)

            self.access_logger.create_success_log("Text injected successfully in description textarea. [object] YoutubeBot [method] __type_in_description_textarea()")

        except Exception as error:

            self.errors_logger.create_error_log(
                f"Exception: {str(error)} [object] YoutubeBot [method] __type_in_description_textarea()")

    def __check_kids_feature(self, driver: uc.Chrome):

        try:
            # Wait until the radio button is present
            radio_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "tp-yt-paper-radio-button[name='VIDEO_MADE_FOR_KIDS_NOT_MFK']")
                )
            )

            # Scroll into view in case it's hidden
            driver.execute_script("arguments[0].scrollIntoView(true);", radio_button)

            # Click it with JS (works better for Polymer elements)
            driver.execute_script("arguments[0].click();", radio_button)

        except Exception as error:

            self.errors_logger.create_error_log(
                f"Exception: {str(error)} [object] YoutubeBot [method] __wait_the_video_to_process()")

    def __wait_the_video_to_process(self, driver: uc.Chrome) -> None:
        try:

            # Wait up to 60 seconds for the text to appear
            element = WebDriverWait(driver, 600).until(
                EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, "span.progress-label.style-scope.ytcp-video-upload-progress"),
                    "Checks complete. No issues found."
                )
            )

            self.access_logger.create_success_log("Video processed without issues. [object] YoutubeBot [method] __wait_the_video_to_process()")

        except Exception as error:

            self.errors_logger.create_error_log(
                f"Exception: {str(error)} [object] YoutubeBot [method] __wait_the_video_to_process()")

    def __details_next_button(self, driver: uc.Chrome) -> None:

        try:
            # Wait for the button to be clickable
            next_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "ytcp-button#next-button button"))
            )

            # Scroll into view (sometimes necessary in YT Studio)
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)

            # Click using JavaScript (most reliable for Polymer elements)
            driver.execute_script("arguments[0].click();", next_button)

            self.access_logger.create_info_log("Moved further from details view. [object] YoutubeBot [method] __details_next_button()")

        except Exception as error:

            self.errors_logger.create_error_log(
                f"Exception: {str(error)} [object] YoutubeBot [method] __details_next_button()")

    def __video_elements_next_button(self, driver: uc.Chrome) -> None:

        try:
            # Wait for the button to be clickable
            next_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "ytcp-button#next-button button"))
            )

            # Scroll into view (sometimes necessary in YT Studio)
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)

            # Click using JavaScript (most reliable for Polymer elements)
            driver.execute_script("arguments[0].click();", next_button)

            self.access_logger.create_info_log("Moved further from video elements view. [object] YoutubeBot [method] __video_elements_next_button()")

        except Exception as error:

            self.errors_logger.create_error_log(
                f"Exception: {str(error)} [object] YoutubeBot [method] __video_elements_next_button()")

    def __checks_next_button(self, driver: uc.Chrome) -> None:

        try:
            # Wait for the button to be clickable
            next_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "ytcp-button#next-button button"))
            )

            # Scroll into view (sometimes necessary in YT Studio)
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)

            # Click using JavaScript (most reliable for Polymer elements)
            driver.execute_script("arguments[0].click();", next_button)

            self.access_logger.create_info_log("Moved further from checks view. [object] YoutubeBot [method] __checks_next_button()")

        except Exception as error:

            self.errors_logger.create_error_log(
                f"Exception: {str(error)} [object] YoutubeBot [method] __checks_next_button()")

    def __mark_public(self, driver: uc.Chrome) -> None:

        try:
            # Wait until the "Public" radio button is clickable
            public_radio = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "tp-yt-paper-radio-button[name='PUBLIC']"))
            )

            # Click the radio button
            public_radio.click()

            self.access_logger.create_info_log("Video marked as public. [object] YoutubeBot [method] __mark_public()")

        except Exception as error:

            self.errors_logger.create_error_log(
                f"Exception: {str(error)} [object] YoutubeBot [method] __mark_public()")

    def __save_video(self, driver: uc.Chrome) -> None:

        save_button = None

        try:
            # Wait for the "Save" button to be clickable
            save_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Save']"))
            )

            # Scroll into view in case it's off-screen
            driver.execute_script("arguments[0].scrollIntoView(true);", save_button)

            save_button.click()

            self.access_logger.create_success_log("Video saved successfully!")

        except Exception as error:
            self.errors_logger.create_error_log(
                f"Attempt to save the video, exception occurred: {str(error)} [object] YoutubeBot [method] __save_video()")

            try:
                # Fallback: force click with JavaScript if Selenium fails
                driver.execute_script("arguments[0].click();", save_button)

                self.access_logger.create_success_log("Video saved successfully!")

                return

            except Exception as error:

                self.errors_logger.create_error_log(
                    f"Exception: {str(error)} [object] YoutubeBot [method] __save_video()")

    def __publish_video(self, driver: uc.Chrome) -> None:

        publish_button = None

        try:
            # Wait until the "Publish" button is clickable
            publish_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Publish']"))
            )

            # Scroll into view if hidden
            driver.execute_script("arguments[0].scrollIntoView(true);", publish_button)

            publish_button.click()

            self.access_logger.create_success_log("Video published successfully!")

        except Exception as error:
            self.errors_logger.create_error_log(
                f"Attempt to save the video, exception occurred: {str(error)} [object] YoutubeBot [method] __publish_video()")

            try:
                # Fallback: force click with JavaScript if Selenium fails
                driver.execute_script("arguments[0].click();", publish_button)

                self.access_logger.create_success_log("Video published successfully!")

                return

            except Exception as error:

                self.errors_logger.create_error_log(
                    f"Exception: {str(error)} [object] YoutubeBot [method] __publish_video()")

    def post_on_youtube(self, profile_path, style_id: int) -> dict:

        try:
            new_video_response = self.get_video(style_id)

            if not 'video-path' in new_video_response:
                self.errors_logger.create_error_log(
                    f"Video path was not created. [object] YoutubeBot [method] post_on_youtube()")

                return {
                    'message': f"Video path was not created. [object] YoutubeBot [method] post_on_youtube()",
                    'status_code': 400
                }

            options = uc.ChromeOptions()
            options.add_argument(f"--user-data-dir={profile_path}")  # user profile folder

            driver = uc.Chrome(options=options)

            driver.get("https://studio.youtube.com")

            self.__click_on_dropdown(driver)
            self.__click_on_upload_button(driver)

            self.__send_video(driver, new_video_response['video-path'])

            self.__type_in_title_textarea(driver, new_video_response['title'])
            self.__type_in_description_textarea(driver, new_video_response['description'])

            self.__check_kids_feature(driver)

            self.__wait_the_video_to_process(driver)

            self.__details_next_button(driver)
            self.__video_elements_next_button(driver)
            self.__checks_next_button(driver)

            self.__mark_public(driver)

            self.__publish_video(driver)
            time.sleep(10)

            driver.quit()

            return {
                'message' : 'Posted successfully',
                'status_code' : 200
            }

        except Exception as error:
            self.errors_logger.create_error_log(
                f"Exception: {str(error)} [object] YoutubeBot [method] get_video()")

            return {
                'message' : f"Exception: {str(error)} [object] YoutubeBot [method] post_on_youtube()",
                'status_code' : 400
            }