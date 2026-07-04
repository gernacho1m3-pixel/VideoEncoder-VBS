import json
import subprocess
from pathlib import Path

FFPROBE_PATH = Path("../ffmpeg/ffprobe.exe")


def get_video_metadata(video_path: str):

    command = [
        str(FFPROBE_PATH),
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        video_path
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    return json.loads(result.stdout)
    