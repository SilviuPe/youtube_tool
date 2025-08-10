import undetected_chromedriver as uc
import time

from selenium.webdriver.common.by import By

# Initialize undetected Chrome
driver = uc.Chrome()
driver.get("https://www.pexels.com/search/videos/hacking/")

time.sleep(3)  # wait for page to load

# Optional: Scroll to load more videos
last_height = driver.execute_script("return document.body.scrollHeight")
for _ in range(3):  # scroll 3 times (adjust as needed)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # wait for new content to load
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Find all download buttons
download_buttons = driver.find_elements(
    By.XPATH, "//a[contains(@class, 'DownloadButton_downloadButton') and contains(., 'Download')]"
)

# Print the links
for btn in download_buttons:
    print(btn.get_attribute("href"))