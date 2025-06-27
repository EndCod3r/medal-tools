import os
from clips_handler import (
    find_clips,
    extract_clips,
    find_clips_by_collection_id,
    find_clips_by_collection_name,
    find_clips_by_title,
)
from downloader import download_clip
from utils.paths import get_default_paths


def main():
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

        # Ask about search type
        print("\nSearch options:")
        print("[1] Search by clip path text")
        print("[2] Search by clip name (contentTitle)")
        print("[3] Search by collection")
        print("[Enter] Copy all clips without search")
        search_type = input(
            "Choose search type (1-3) or press Enter to copy all: "
        ).strip()

        if search_type == "1":
            search_string = input("Enter text to search in clip path: ").strip().lower()
            clips = find_clips(json_path)
            if search_string:
                clips = [
                    clip
                    for clip in clips
                    if search_string in os.path.basename(clip).lower()
                ]
        elif search_type == "2":
            search_string = input("Enter clip name to search for: ").strip().lower()
            clips = find_clips_by_title(json_path, search_string)
        elif search_type == "3":
            print("\nEnter collection type:")
            print("[1] Search by collection ID")
            print("[2] Search by collection name")
            collection_choice = input("Choose option (1/2): ").strip()

            if collection_choice == "1":
                collection_id = input("Enter collection ID to search for: ").strip()
                if collection_id:
                    clips = find_clips_by_collection_id(json_path, collection_id)
            elif collection_choice == "2":
                collection_name = (
                    input("Enter collection name to search for: ").strip().lower()
                )
                clips = find_clips_by_collection_name(json_path, collection_name)
        else:
            clips = find_clips(json_path)

        if not clips:
            print("No matching clips found.")
            return

        extract_clips(clips, os.path.abspath(target_dir))
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
