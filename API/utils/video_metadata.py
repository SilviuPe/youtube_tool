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


        ffmpeg_command = (f"ffmpeg -i {input_file} "
                          f"-vf {block_video_metadata['resolution']} "
                          f"-c:v {block_video_metadata['codec_video']} "
                          f"-profile:v {block_video_metadata['codec_profile_video']} "
                          f"-level {block_video_metadata['codec_video_level']} "
                          f"-pix_fmt {block_video_metadata['pixel_format']} "
                          f"-crf {block_video_metadata['crf']} "
                          f"-preset {block_video_metadata['preset']} "
                          f"-movflags {block_video_metadata['movflags']} "
                          f"-an "
                          f"-r {block_video_metadata['fps']} "
                          f"-y temp_output.mp4 && mv -f temp_output.mp4 {input_file} ")


        subprocess.run(ffmpeg_command, capture_output=True, text=True)

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