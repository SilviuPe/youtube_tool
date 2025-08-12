import requests, os

CURRENT_PATH_FILE = os.path.abspath(__file__)
CURRENT_PATH = os.path.dirname(CURRENT_PATH_FILE)

from ClipsFromWeb.Pexels.main import PexelsScraper

# json_data = {
#     'category' : 'car',
#     'video_qt' : 3,
#     'audio_script': "Alright, here’s one for you—if you’re cruising at 60 mph and you glance at your phone for just 5 seconds, you’ve basically just driven the length of a football field without looking. Kinda like closing your eyes while sprinting… but in a two-ton metal box."
# }
# #109.176.199.63
# # 192.168.0.108
# res = requests.post('http://109.176.199.63:5000/get-random-video', json=json_data, stream=True)
#
# if res.status_code == 200:
#     with open(f"{CURRENT_PATH}\\received_video.mp4", "wb") as f:
#         for chunk in res.iter_content(chunk_size=8192):
#             if chunk:  # ignore keep-alive chunks
#                 f.write(chunk)
# else:
#     print(f"Error: {res.status_code} - {res.text}")


tool = PexelsScraper()

videos = tool.get_new_videos("keyboard", 10)

res = requests.post('http://109.176.199.63:5000/save-new-data', json=videos)

print(res.content.decode())

