import os
import subprocess
import ffmpeg

def merge_audio(original_video, video_no_audio, output_video):
    try:
        probe = ffmpeg.probe(original_video)
        has_audio = any(stream['codec_type'] == 'audio' for stream in probe['streams'])

        if not has_audio:
            os.rename(video_no_audio, output_video)
            return

        temp_audio = f"{output_video}_audio.aac"
        extract_cmd = [
            "ffmpeg", "-y", "-i", original_video, "-vn", "-acodec", "copy", temp_audio
        ]
        subprocess.run(extract_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        merge_cmd = [
            "ffmpeg", "-y", "-i", video_no_audio, "-i", temp_audio,
            "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", output_video
        ]
        subprocess.run(merge_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        os.remove(temp_audio)

    except Exception as e:
        print("Audio merge failed:", str(e))
        os.rename(video_no_audio, output_video)



