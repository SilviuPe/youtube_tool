import os
import io
import uuid
from pydub import AudioSegment
import edge_tts

from .log.logger import Logger

# Ensure pydub uses correct ffmpeg paths
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffmpeg = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"

CURRENT_PATH_FILE = os.path.abspath(__file__)
CURRENT_PATH = os.path.dirname(CURRENT_PATH_FILE)


class VoiceGeneratorWindowsEdge:
    def __init__(self):
        self.success_logger = Logger(f"{CURRENT_PATH}\\log\\access.log")
        self.error_logger = Logger(f"{CURRENT_PATH}\\log\\errors.log")

    async def _generate_voice(self, text: str, voice_params: dict, voice="en-CA-LiamNeural") -> AudioSegment:
        """
        Generate voice using edge-tts and apply audio adjustments.
        voice_params example:
        {
            "pitch_shift": 0.65,
            "low_pass_cutoff": 1200,
            "channels": 1,
            "sample_width": 2,
            "gain_db": 6
        }
        """
        try:
            communicate = edge_tts.Communicate(text, voice)

            # Use a unique temp file in TEMP folder
            temp_file = os.path.join(os.getenv("TEMP"), f"{uuid.uuid4()}.mp3")
            await communicate.save(temp_file)

            audio = AudioSegment.from_file(temp_file, format="mp3")

            # Apply voice adjustments dynamically
            audio = audio.set_frame_rate(int(audio.frame_rate * voice_params.get("pitch_shift", 1.0)))
            audio = audio.low_pass_filter(voice_params.get("low_pass_cutoff", 20000))
            audio = audio.set_channels(voice_params.get("channels", 2))
            audio = audio.set_sample_width(voice_params.get("sample_width", 2))
            audio = audio + voice_params.get("gain_db", 0)

            os.remove(temp_file)
            return audio

        except Exception as e:
            self.error_logger.create_error_log(
                f"Exception: {str(e)}. [object] VoiceGeneratorWindowsEdge [method] _generate_voice()"
            )
            return AudioSegment.silent(duration=1000)

    def _generate_empty(self, duration: int) -> AudioSegment:
        return AudioSegment.silent(duration=duration * 1000)

    def _generate_sound(self, sound: str) -> AudioSegment:
        sound_file = os.path.join(self.sounds_folder, f"{sound}.wav")
        if os.path.exists(sound_file):
            return AudioSegment.from_file(sound_file, format="wav")
        else:
            return AudioSegment.silent(duration=1000)

    async def generate_audio(
        self,
        audio_script: list,
        voice_params: dict | None = None,
        voice_name: str | None = None
    ) -> list:
        try:
            if not voice_name:
                voice_name = "en-US-AriaNeural"

            if not voice_params:
                voice_params = {
                    "pitch_shift": 1.0,
                    "low_pass_cutoff": 20000,
                    "channels": 2,
                    "sample_width": 2,
                    "gain_db": 0
                }

            final_audio = AudioSegment.silent(duration=0)

            for part in audio_script:
                if part["type"] == "voice":
                    clip = await self._generate_voice(part["text"], voice_params=voice_params, voice=voice_name)
                elif part["type"] == "empty":
                    clip = self._generate_empty(part["duration"])
                elif part["type"] == "sound":
                    clip = self._generate_sound(part["sound"])
                else:
                    clip = AudioSegment.silent(duration=0)

                final_audio += clip

            audio_bytes = io.BytesIO()
            final_audio.export(audio_bytes, format="mp3")
            audio_bytes.seek(0)

            bytes_content = audio_bytes.getvalue()
            duration = AudioSegment.from_file(io.BytesIO(bytes_content)).duration_seconds

            return [{"audio_bytes": bytes_content, 'duration' : duration}, 200]

        except Exception as error:
            self.error_logger.create_error_log(
                f"Exception: {str(error)}. [object] VoiceGeneratorWindowsEdge [method] generate_audio()"
            )
            return [{"error": str(error)}, 400]
