import requests, os

CURRENT_PATH_FILE = os.path.abspath(__file__)
CURRENT_PATH = os.path.dirname(CURRENT_PATH_FILE)

# /get-random-video
#
json_data = {
    'category' : 'hacking',
    'video_qt' : 3,
    'audio_script': "Alright, here’s one for you—if a hacker gets your email password, they can often reset every other account you own in under 10 minutes. It’s like giving someone the master key to your entire life… plus the spare, plus the one you didn’t even know existed."
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
#

# /save-new-data

# from ClipsFromWeb.Pexels.main import PexelsScraper
#
# tool = PexelsScraper()
#
# videos = tool.get_new_videos("hacking", 10)
#
# res = requests.post('http://109.176.199.63:5000/save-new-data', json=videos)
#
# print(res.content.decode())

