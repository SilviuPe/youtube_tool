import os
import io
from pydub import AudioSegment
import edge_tts

from .log.logger import Logger


AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffmpeg = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"

CURRENT_PATH_FILE = os.path.abspath(__file__)
CURRENT_PATH = os.path.dirname(CURRENT_PATH_FILE)


class VoiceGeneratorWindowsEdge:

    def __init__(self) -> None:
        self.success_logger = Logger(f"{CURRENT_PATH}\\log\\access.log")
        self.error_logger = Logger(f"{CURRENT_PATH}\\log\\errors.log")

    async def _generate_voice(self, text: str, voice_params: dict, voice="en-CA-LiamNeural") -> AudioSegment:

        """
        {
            "pitch_shift": 0.65,  # Factor de schimbare a pitch-ului (0.65 înseamnă scădere semnificativă)
            "low_pass_cutoff": 1200,  # Frecvența de tăiere pentru filtrul low-pass (în Hz)
            "channels": 1,  # Numărul de canale (1 pentru mono)
            "sample_width": 2,  # Adâncimea de bit (2 pentru 16-bit)
            "gain_db": 6  # Amplificare în dB
        }
        """

        communicate = edge_tts.Communicate(text, voice)
        temp_file = "temp_audio.mp3"
        await communicate.save(temp_file)
        audio = AudioSegment.from_file(temp_file, format="mp3")

        new_sample_rate = int(audio.frame_rate * voice_params["pitch_shift"])
        audio = audio.set_frame_rate(new_sample_rate)

        # Filtru low-pass
        audio = audio.low_pass_filter(voice_params["low_pass_cutoff"])

        # Setări canale și adâncime de bit
        audio = audio.set_channels(voice_params["channels"])
        audio = audio.set_sample_width(voice_params["sample_width"])

        # Amplificare volum
        audio = audio + voice_params["gain_db"]

        os.remove(temp_file)  # Șterge fișierul temporar
        return audio

    def _generate_empty(self, duration: int) -> AudioSegment:
        return AudioSegment.silent(duration=duration * 1000)

    def _generate_sound(self, sound: str) -> AudioSegment:
        sound_file = os.path.join(self.sounds_folder, f"{sound}.wav")
        if os.path.exists(sound_file):
            return AudioSegment.from_file(sound_file, format="wav")
        else:
            return AudioSegment.silent(duration=1000)

    async def generate_audio(self, audio_script: list, voice_params: dict | None, voice_name: str | None) -> list:
        try:

            if not voice_name:
                voice_name = "en-US-AriaNeural"
            if not voice_params:
                voice_params = {
                    "pitch_shift": 1.0,  # No pitch shift
                    "low_pass_cutoff": 20000,  # Allow all frequencies (20 kHz is the upper limit of human hearing)
                    "channels": 2,  # Stereo output
                    "sample_width": 2,  # 16-bit depth (standard for CD-quality audio)
                    "gain_db": 0  # No gain adjustment
                }

            final_audio = AudioSegment.silent(duration=0)

            for part in audio_script:
                if part["type"] == "voice":
                    clip = await self._generate_voice(part["text"], voice=voice_name, voice_params=voice_params)
                elif part["type"] == "empty":
                    clip = self._generate_empty(part["duration"])
                elif part["type"] == "sound":
                    clip = self._generate_sound(part["sound"])
                else:
                    clip = AudioSegment.silent(duration=0)

                final_audio += clip

            audio_bytes = io.BytesIO()
            final_audio.export(audio_bytes, format="mp3")
            audio_bytes.seek(0)  # Rewind to the beginning of the BytesIO object

            return [{"audio_bytes": audio_bytes.getvalue()}, 200]

        except Exception as error:

            self.error_logger.create_error_log(f"Exception: {str(error)}. [object] VoiceGeneratorWindowsEdge [method] generate_audio()")

            return [{"error" : str(error)}, 400]


# async def list_all_voices():
#     voices = await edge_tts.list_voices()
#     for voice in voices:
#         if voice['Gender'] == 'Male' and 'en' in voice['Locale']:
#             print(f"ShortName: {voice['ShortName']}, Locale: {voice['Locale']}, Gender: {voice['Gender']}")



# audio_params = {
#     "pitch_shift": 0.65,  # Factor de schimbare a pitch-ului (0.65 înseamnă scădere semnificativă)
#     "low_pass_cutoff": 1200,  # Frecvența de tăiere pentru filtrul low-pass (în Hz)
#     "channels": 1,  # Numărul de canale (1 pentru mono)
#     "sample_width": 2,  # Adâncimea de bit (2 pentru 16-bit)
#     "gain_db": 6  # Amplificare în dB
# }


# if cmd == 'run':
#
#     # Example usage
#     audio_script = [
#
#             {
#                 "type": "empty",
#                 "duration": 2
#             },
#             {
#                 "type": "voice",
#                 "text": "In the shadows, hackers paint a digital canvas."
#             },
#             {
#                 "type": "voice",
#                 "text": "With every keystroke, they break barriers."
#             },
#             {
#                 "type": "voice",
#                 "text": "But remember, with power comes responsibility."
#             },
#             {
#                 "type": "empty",
#                 "duration": 2
#             },
#             {
#                 "type": "voice",
#                 "text": "Are you ready to join the ranks?"
#             }
#
#     ]