import subprocess
import re
from pathlib import Path

from app.services.progress_service import set_progress


FFMPEG_PATH = Path("../ffmpeg/ffmpeg.exe")
UPLOAD_FOLDER = Path("uploads")
OUTPUT_FOLDER = Path("output")

OUTPUT_FOLDER.mkdir(exist_ok=True)


def convert_video(
    filename: str,
    output_format: str,
    vcodec: str,
    resolution: str,
    fps: int,
    vbitrate: int,
    abitrate: int
):

    input_path = UPLOAD_FOLDER / filename
    output_file = f"{input_path.stem}_converted.{output_format}"
    output_path = OUTPUT_FOLDER / output_file

    scale = {
        "original": "scale=iw:ih",
        "720p": "scale=1280:720",
        "1080p": "scale=1920:1080",
        "1440p": "scale=2560:1440"
    }.get(resolution, "scale=iw:ih")

    cmd = [
        str(FFMPEG_PATH),
        "-i", str(input_path),

        "-c:v", vcodec,
        "-b:v", f"{vbitrate}k",

        "-c:a", "aac",
        "-b:a", f"{abitrate}k",

        "-vf", scale,
        "-r", str(fps),

        "-y",
        str(output_path)
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    duration = None

    for line in process.stderr:

        if duration is None:
            m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", line)

            if m:
                h = int(m.group(1))
                mnt = int(m.group(2))
                sec = float(m.group(3))

                duration = h * 3600 + mnt * 60 + sec

        t = re.search(r"time=(\d+):(\d+):(\d+\.\d+)", line)

        if t and duration:
            h = int(t.group(1))
            mnt = int(t.group(2))
            sec = float(t.group(3))

            current = h * 3600 + mnt * 60 + sec

            percent = int(current / duration * 100)

            if percent > 100:
                percent = 100

            set_progress(filename, percent)

    process.wait()

    set_progress(filename, 100)

    return str(output_file)