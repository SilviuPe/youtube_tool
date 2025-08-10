import requests
import platform

from flask import Flask, request

from Database.main import DatabaseConnection

app = Flask(__name__)


slash = '\\'
if platform.system() == 'Linux':
    slash = "/"  # path of the sql Queries folder

def download_video(url: str, name: str, path: str = "/home/videos/pexels"):
    with requests.get(url, stream=True) as r:
        with open(f"{path}{slash}{name}.mp4", 'wb') as f:
            for ck in r.iter_content(chunk_size=8192):
                f.write(ck)
            f.close()

    return f"{path}{slash}{name}.mp4"


@app.route("/save_new_data", methods=["POST"])
def upload_video():
    try:
        data = request.get_json()

        if data:

            try:
                db = DatabaseConnection()

                for video in data:
                    if "save_data" in video:

                        if "filename" in video["save_data"]:
                            file_path = download_video(video['download_link'],video["save_data"]["filename"])

                            del data['save_data']

                            data.update({"video_path" : file_path})

                            db.add_pexels_video(data=data)

                return "Data Added Successfully", 200

            except Exception as error:
                return f"Error: {str(error)}", 400

        else:
            return "No data was provided", 400

    except Exception as error:
            return f"Error: {str(error)}", 400



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
