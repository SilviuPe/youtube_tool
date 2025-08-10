import requests

from flask import Flask, request

from Database.main import DatabaseConnection

app = Flask(__name__)


def download_video(url: str, name: str, path: str = "/home/videos/pexels"):
    with requests.get(url, stream=True) as r:
        with open(f"{path}\\{name}.mp4", 'wb') as f:
            for ck in r.iter_content(chunk_size=8192):
                f.write(ck)
            f.close()


@app.route("/save_new_data", methods=["POST"])
def upload_video():
    try:
        data = request.get_json()

        try:
            db = DatabaseConnection()

            print(db)
            #db.add_pexels_video(data=data)

            return "Data Added Successfully", 200

        except Exception as error:
            return f"Error: {str(error)}", 400

    except Exception as error:
            return f"Error: {str(error)}", 400



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
