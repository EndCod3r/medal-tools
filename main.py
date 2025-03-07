import os
from clips_handler import find_clips, extract_clips
from downloader import download_clip
from utils.paths import get_default_paths


def main():
    # Get path configuration
    paths = get_default_paths()
    default_clips_dir = paths["default_clips_dir"]
    default_json_path = paths["default_json_path"]

    print("[1] Copy local clips to directory")
    print("[2] Download clip from URL")
    choice = input("Select option: ").strip()

    if choice == "1":
        json_path = (
            input(
                f"Enter custom clips.json path [Enter for default ({default_json_path})]: "
            ).strip()
            or default_json_path
        )

        target_dir = (
            input(f"Where to save clips? [Enter for {default_clips_dir}]: ").strip()
            or default_clips_dir
        )

        # Ask about filtering
        filter_clips = input("Filter clips by name? (y/n): ").lower().strip()
        search_string = ""
        if filter_clips == "y":
            search_string = (
                input("Enter text to search in clip names: ").strip().lower()
            )

        clips = find_clips(json_path)

        if clips:
            # Apply filter if requested
            if search_string:
                filtered_clips = [
                    clip
                    for clip in clips
                    if search_string in os.path.basename(clip).lower()
                ]
                if not filtered_clips:
                    print(
                        f"No clips found containing '{search_string}' in their names."
                    )
                    return
                clips = filtered_clips

            extract_clips(clips, os.path.abspath(target_dir))
        else:
            print("No valid clips found in the JSON file.")

    elif choice == "2":
        url = input("Enter Medal.tv clip URL: ").strip()
        target_dir = (
            input(f"Where to save downloads? [Enter for {default_clips_dir}]: ").strip()
            or default_clips_dir
        )

        os.makedirs(target_dir, exist_ok=True)

        if download_clip(url, os.path.abspath(target_dir)):
            print("Download completed successfully!")
        else:
            print("Download failed")

    else:
        print("Invalid selection.")


if __name__ == "__main__":
    main()
