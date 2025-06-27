import os
import re

# Set this to your folder with clips
FOLDER = r"./Clips"

# Regex to match the naming format with optional -tr-edit
pattern = re.compile(
    r"MedalTV.+?(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})(?:-tr-edit)?\.(mp4|mkv)",
    re.IGNORECASE,
)

for filename in os.listdir(FOLDER):
    match = pattern.fullmatch(filename)
    if match:
        year, month, day, hour, minute, second, ext = match.groups()
        short_year = year[-2:]  # Get last 2 digits
        new_name = f"{month}-{day}-{short_year} {hour}-{minute}-{second}.{ext}"
        src = os.path.join(FOLDER, filename)
        dst = os.path.join(FOLDER, new_name)
        try:
            os.rename(src, dst)
            print(f"Renamed: {filename} -> {new_name}")
        except Exception as e:
            print(f"Error renaming {filename}: {e}")
