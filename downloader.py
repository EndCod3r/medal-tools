import subprocess
import os


def download_clip(url, output_dir):
    """Downloads a clip using yt-dlp with real-time progress"""
    downloader_exe = "yt-dlp.exe"
    options = [
        "--no-mtime",
        "--add-metadata",
        "--progress",
        "--newline",
        "-o",
        os.path.join(output_dir, "[%(id)s] %(title)s.%(ext)s"),
    ]

    if not os.path.isfile(downloader_exe):
        print(f"Error: {downloader_exe} not found in current directory")
        return False

    try:
        command = [downloader_exe, url] + options
        print("Starting download...")

        with subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        ) as process:
            for line in process.stdout:
                print(line.strip(), flush=True)

            return_code = process.wait()

        return return_code == 0

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False
