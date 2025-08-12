import requests
import platform
import os
import random
import io

from flask import Flask, request, send_file
from typing_extensions import override

from Database.main import DatabaseConnection
from GenerateVideo.main import ManualVideoGenerator
from .utils.video_metadata import VideoMetaData

app = Flask(__name__)

CURRENT_PATH_FILE = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(CURRENT_PATH_FILE)

slash = '\\'
default_path = f"{CURRENT_DIR}"

if platform.system() == 'Linux':
    slash = "/"  # path of the sql Queries folder
    default_path = "/home/videos/pexels"

def download_video(url: str, name: str, path: str = default_path):
    with requests.get(url, stream=True) as r:
        with open(f"{path}{slash}{name}.mp4", 'wb') as f:
            for ck in r.iter_content(chunk_size=8192):
                f.write(ck)
            f.close()

    return f"{path}{slash}{name}.mp4"


@app.route("/save-new-data", methods=["POST"])
def upload_video():
    try:
        data = request.get_json()

        if data:

            try:
                db = DatabaseConnection()
                v_metadata_tool = VideoMetaData()
                db_data = []
                for video in data:
                    if "save_data" in video:
                        if "filename" in video["save_data"]:
                            file_path = download_video(video['download_link'],video["save_data"]["filename"])
                            v_metadata_tool.change_metadata(data={'file_path' : file_path})

                            del video['save_data']

                            video.update({"video_path" : file_path})
                            db_data.append(video)

                db.add_pexels_video(data=db_data)

                return "Data Added Successfully", 200

            except Exception as error:
                return f"Error: {str(error)}", 400

        else:
            return "No data was provided", 400

    except Exception as error:
            return f"Error: {str(error)}", 400


@app.route('/get-random-video', methods=['GET', 'POST'])
def get_random_video():

    if request.method == 'GET':
        try:

            db = DatabaseConnection()

            random_video_id = random.randint(33,54)

            db_video_path = db.request_pexels_video(video_path=True, conditions={"id" : random_video_id})[0]['video_path']

            return send_file(db_video_path)

        except Exception as error:
            return f"Error: {str(error)}", 400

    elif request.method == 'POST':

        try:

            db = DatabaseConnection()
            video_tool = ManualVideoGenerator()

            try:

                data = request.get_json()
                conditions = {}
                video_quantity = 0
                random_ids = []
                video_paths = []
                audio_script = ''
                if "audio_script" in data:
                    audio_script = data['audio_script']
                else:
                    return "audio_script is missing", 400

                if "category" in data:
                    conditions.update({"key_word_search": data['category']})
                else:
                    return "category is missing", 400

                video_data = video_tool.define_video_data(audio_script)

                video_quantity = video_data['video_qt']
                last_video_duration = video_data['last_video_duration']
                audio_bytes = video_data['audio_bytes']

                while len(random_ids) < video_quantity:

                    random_id = random.randint(56,65)

                    if random_id not in random_ids:
                        random_ids.append(random_id)
                    else:
                        continue

                for id_ in random_ids:

                    video_path = db.request_pexels_video(video_path=True, conditions={"id" : id_, **conditions})[0]['video_path']
                    video_paths.append(video_path)

                video_bytes = video_tool.generate_video(video_paths, audio_bytes, last_video_duration)


                return send_file(io.BytesIO(video_bytes), mimetype="video/mp4", as_attachment=True, download_name="video.mp4")

            except Exception as error:

                return f"Exception: {str(error)}", 400



        except Exception as error:
            return f"Exception: {str(error)}", 400

    else:

        return f"Method not allowed"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
