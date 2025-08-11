import requests, os

CURRENT_PATH_FILE = os.path.abspath(__file__)
CURRENT_PATH = os.path.dirname(CURRENT_PATH_FILE)

json_data = {
    'category' : 'car',
    'video_qt' : 10
}

res = requests.post('http://109.176.199.63:5000/get-random-video', stream=True)

with open(f"{CURRENT_PATH}\\videos.zip", 'wb') as f:
    for chunk in res.iter_content(chunk_size=8192):
        f.write(chunk)
    f.close()
