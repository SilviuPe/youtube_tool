import subprocess
import tempfile
import base64
import re

def write_bytes_to_file(byte_data, filepath):
    with open(filepath, 'wb') as f:
        f.write(byte_data)


def get_media_duration(audio_bytes):

    with tempfile.TemporaryDirectory() as tmpdir:
        # Save audio bytes to a WAV file (assuming voice is raw audio bytes)
        audio_path = f"{tmpdir}\\audio.wav"
        write_bytes_to_file(audio_bytes, audio_path)

        """ Get media duration in seconds using ffprobe """
        cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{audio_path}"'
        duration = subprocess.check_output(cmd, shell=True).decode().strip()
        return float(duration)


def base64_to_video(base64_string: str, output_path: str) -> None:
    """
    Decode a Base64 string and save it as an MP4 file.
    """
    # Strip metadata prefix if exists
    if ',' in base64_string:
        base64_string = base64_string.split(',', 1)[1]

    # Remove any invalid characters
    base64_string = re.sub(r'[^A-Za-z0-9+/=]', '', base64_string)

    # Fix padding
    base64_string += '=' * ((4 - len(base64_string) % 4) % 4)

    # Decode & write
    with open(output_path, 'wb') as f:
        f.write(base64.b64decode(base64_string))

def video_to_base64(path_of_video: str) -> str:
    """
    Read an MP4 file and return its Base64 string representation.
    """
    with open(path_of_video, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')