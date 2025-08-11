import requests
import platform
import os
import random
import io
import zipfile

from flask import Flask, request, send_file

from Database.main import DatabaseConnection

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
                db_data = []
                for video in data:
                    if "save_data" in video:
                        if "filename" in video["save_data"]:
                            file_path = download_video(video['download_link'],video["save_data"]["filename"])

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

            try:

                data = request.get_json()
                conditions = {}
                video_quantity = 0
                random_ids = []
                video_paths = []

                if "category" in data:
                    conditions.update({"key_word_search": data['category']})

                if "video_qt" in data:
                    video_quantity = data['video_qt']
                else:
                    video_quantity = 1



                while len(random_ids) < video_quantity:

                    random_id = random.randint(33,54)

                    if random_id not in random_ids:
                        random_ids.append(random_id)
                    else:
                        continue

                if not len(conditions):
                    conditions = None

                for id_ in random_ids:

                    video_path = db.request_pexels_video(video_path=True, conditions=conditions.update({"id" : id_}))[0]['video_path']
                    video_paths.append(video_path)

                memory_file = io.BytesIO()

                with zipfile.ZipFile(memory_file, 'w') as zf:
                    for filepath in video_paths:
                        zf.write(filepath, arcname=filepath.split("/")[-1])
                memory_file.seek(0)

                return send_file(memory_file, mimetype='application/zip', download_name='videos.zip')

            except Exception as error:

                return f"Exception: {str(error)}", 400



        except Exception as error:
            return f"Exception: {str(error)}", 400

    else:

        return f"Method not allowed"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
