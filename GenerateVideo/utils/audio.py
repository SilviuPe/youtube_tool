import subprocess
import tempfile

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