import os
import subprocess

class VideoMetaData(object):

    def __init__(self):
        self.default_video_stream_data = {
            "resolution": "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1",
            "codec_video": "libx264",
            "codec_video_level": "4.2",
            "codec_profile_video": "high",
            "pixel_format": "yuv420p",
            "crf" : "18",
            "preset": "fast",
            "movflags": "+faststart",
            "fps": "60"
        }
    def change_metadata(self, data : dict):
        """
        Method to change the resolution of a video
        :param: override - bool to change the file or create a new one
        """
        input_file = data["file_path"]

        block_video_metadata = {**self.default_video_stream_data}

        for setting in list(self.default_video_stream_data.keys()):

            if setting in data:

                block_video_metadata[setting] = data[setting]

        ffmpeg_command = [
            "ffmpeg",
            "-i", input_file,
            "-vf", block_video_metadata['resolution'],
            "-c:v", block_video_metadata['codec_video'],
            "-profile:v", block_video_metadata['codec_profile_video'],
            "-level", block_video_metadata['codec_video_level'],
            "-pix_fmt", block_video_metadata['pixel_format'],
            "-crf", str(block_video_metadata['crf']),  # Ensure it's string if number
            "-preset", block_video_metadata['preset'],
            "-movflags", block_video_metadata['movflags'],
            "-an",
            "-r", str(block_video_metadata['fps']),  # Ensure it's string if number
            "-y",
            "temp_output.mp4",
        ]

        override_command = f'mv -f temp_output.mp4 "{input_file}"'

        print(" ".join(ffmpeg_command))

        command_result = subprocess.run(ffmpeg_command, capture_output=True, text=True)
        override_command_result = os.system(override_command)

        if command_result.returncode != 0:
            print("FFmpeg Error:", command_result.stderr)

"""
ffmpeg -i input.mp4 \
       -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1" \
       -c:v libx264 \
       -profile:v high \
       -level 4.2 \
       -pix_fmt yuv420p \
       -crf 18 \
       -preset fast \
       -movflags +faststart \
       -c:a aac -b:a 192k \
       -r 60 \
       output_shorts.mp4
"""