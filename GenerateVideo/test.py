import requests, os

CURRENT_PATH_FILE = os.path.abspath(__file__)
CURRENT_PATH = os.path.dirname(CURRENT_PATH_FILE)

# # /get-random-video
# #
json_data = {
    'category' : 'mountain route',
    'video_qt' : 4,
    'audio_script': "When hiking a mountain trail, always check the weather forecast before starting. Wear sturdy footwear, carry enough water, and follow marked paths to avoid getting lost. Start early in the day, pace yourself, and respect nature—leave no trash behind so others can enjoy the same beauty."
}
#109.176.199.63
# 192.168.0.108
res = requests.post('http://109.176.199.63:5000/get-random-video', json=json_data, stream=True)

if res.status_code == 200:
    with open(f"{CURRENT_PATH}\\received_video.mp4", "wb") as f:
        for chunk in res.iter_content(chunk_size=8192):
            if chunk:  # ignore keep-alive chunks
                f.write(chunk)
else:
    print(f"Error: {res.status_code} - {res.text}")


# /save-new-data

# from ClipsFromWeb.Pexels.main import PexelsScraper
#
# tool = PexelsScraper()
#
# videos = tool.get_new_videos("mountain route", 10)
#
# res = requests.post('http://109.176.199.63:5000/save-new-data', json=videos)
#
# print(res.content.decode())

