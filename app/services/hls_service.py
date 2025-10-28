import subprocess
from pathlib import Path
from typing import List

def generate_hls(input_path: Path) -> Path:
    """Generate multi-bitrate HLS streams and master manifest."""
    output_dir = input_path.parent / input_path.stem
    output_dir.mkdir(exist_ok=True)

    # FFmpeg command for 3 resolutions (240p, 480p, 720p)
    cmd = [
        "ffmpeg", "-y", "-i", str(input_path),
        "-filter_complex",
        "[v:0]split=3[v1][v2][v3];"
        "[v1]scale=426:240[v1out];"
        "[v2]scale=854:480[v2out];"
        "[v3]scale=1280:720[v3out]",
        "-map", "[v1out]", "-map", "a:0", "-c:v:0", "libx264", "-b:v:0", "400k",
        "-map", "[v2out]", "-map", "a:0", "-c:v:1", "libx264", "-b:v:1", "800k",
        "-map", "[v3out]", "-map", "a:0", "-c:v:2", "libx264", "-b:v:2", "1500k",
        "-f", "hls",
        "-hls_time", "4",
        "-hls_playlist_type", "vod",
        "-hls_segment_filename", str(output_dir / "%v_%03d.ts"),
        "-master_pl_name", "master.m3u8",
        "-var_stream_map", "v:0,a:0 v:1,a:1 v:2,a:2",
        str(output_dir / "%v.m3u8")
    ]

    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output_dir
