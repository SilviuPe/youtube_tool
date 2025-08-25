import platform
import os
import asyncio
from flask import Flask, request, jsonify
from GenerateVoice.windows import VoiceGeneratorWindowsEdge

app = Flask(__name__)

CURRENT_PATH_FILE = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(CURRENT_PATH_FILE)

slash = '\\'
default_path = f"{CURRENT_DIR}"

if platform.system() == 'Linux':
    slash = "/"  # path of the sql Queries folder

@app.route('/create-audio', methods=['POST'])
async def create_voice():
    if request.method == 'POST':
        try:
            data = request.get_json(force=True)
            if 'audio_script' not in data:
                return jsonify({"error": "Missing audio_script parameter."}), 400

            voice_tool = VoiceGeneratorWindowsEdge()
            voice_params = data.get('voice_params', None)
            voice_name = data.get('voice_name', None)

            generated_voice = await voice_tool.generate_audio(data['audio_script'], voice_params, voice_name)

            if generated_voice[1] == 200:
                return generated_voice[0]["audio_bytes"], 200
            else:
                return jsonify({"error": "Failed to generate voice."}), 500

        except Exception as error:
            return jsonify({"error": str(error)}), 400
    else:
        return jsonify({"error": "Method not allowed."}), 405

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=44534)
