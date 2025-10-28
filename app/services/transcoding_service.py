import subprocess
from pathlib import Path
from typing import List

# target resolutions and bitrates
TARGETS = [
    ("240p", "426x240", "400k"),
    ("480p", "854x480", "800k"),
    ("720p", "1280x720", "1500k"),
]

def transcode_video(input_path: Path) -> List[Path]:
    """Transcode a video file into multiple resolutions."""
    output_files = []

    # create subfolder to store transcoded versions
    output_dir = input_path.parent / input_path.stem
    output_dir.mkdir(exist_ok=True)

    for label, resolution, bitrate in TARGETS:
        output_file = output_dir / f"{input_path.stem}_{label}.mp4"
        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_path),
            "-vf", f"scale={resolution}",
            "-b:v", bitrate,
            "-c:a", "aac",
            "-c:v", "libx264",
            "-preset", "veryfast",
            str(output_file)
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output_files.append(output_file)

    return output_files
