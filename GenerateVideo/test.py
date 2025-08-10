import os

from GenerateVoice.main import GenerateVoice

CURRENT_PATH_FILE = os.path.abspath(__file__)
CURRENT_PATH = os.path.dirname(CURRENT_PATH_FILE)

tool = GenerateVoice(api_key=os.getenv("ELEVENLABS_API_KEY"), voice_id="29vD33N1CtxCmqQRPOHJ")

voice = tool.generate_voice("Hello everyone! Did you hear about this new feature from Facebook?")[0]['audio_object']

tool.write_out_voice(voice, output_path=f"{CURRENT_PATH}\\output.mp3")