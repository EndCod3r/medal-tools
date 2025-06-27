import argparse
import os
import sys
from utils.clips_handler import (
    find_clips,
    extract_clips,
    find_clips_by_collection_id,
    find_clips_by_collection_name,
    find_clips_by_title,
)
from utils.downloader import download_clip
from utils.paths import get_default_paths


def handle_copy_mode(args):
    json_path = args.json
    target_dir = args.copy_dir
    clips = []

    if args.path_text:
        all_clips = find_clips(json_path)
        clips = [
            clip
            for clip in all_clips
            if args.path_text.lower() in os.path.basename(clip).lower()
        ]
    elif args.title:
        clips = find_clips_by_title(json_path, args.title.lower())
    elif args.collection_id:
        clips = find_clips_by_collection_id(json_path, args.collection_id)
    elif args.collection_name:
        clips = find_clips_by_collection_name(json_path, args.collection_name.lower())
    else:
        clips = find_clips(json_path)

    if not clips:
        print("No matching clips found.")
        return

    extract_clips(clips, os.path.abspath(target_dir))
    print(f"Copied {len(clips)} clips to {target_dir}")


def handle_download_mode(args):
    os.makedirs(args.save_dir, exist_ok=True)
    if download_clip(args.url, os.path.abspath(args.save_dir)):
        print("Download completed successfully!")
    else:
        print("Download failed.")


def interactive_menu():
    paths = get_default_paths()
    default_clips_dir = paths["default_clips_dir"]
    default_json_path = paths["default_json_path"]

    print("[1] Copy local clips to directory")
    print("[2] Download clip from URL")
    choice = input("Select option: ").strip()

    if choice == "1":
        json_path = (
            input(f"Enter JSON path [Enter for {default_json_path}]: ").strip()
            or default_json_path
        )
        copy_dir = (
            input(f"Save clips where? [Enter for {default_clips_dir}]: ").strip()
            or default_clips_dir
        )

        print("\nSearch options:")
        print("[1] Search by clip path text")
        print("[2] Search by clip title")
        print("[3] Search by collection")
        print("[Enter] Copy all clips")
        search_type = input("Choose search type (1-3) or press Enter: ").strip()

        args = argparse.Namespace(
            json=json_path,
            copy_dir=copy_dir,
            path_text=None,
            title=None,
            collection_id=None,
            collection_name=None,
        )

        if search_type == "1":
            args.path_text = input("Enter text to search in clip path: ").strip()
        elif search_type == "2":
            args.title = input("Enter clip title to search: ").strip()
        elif search_type == "3":
            print("\n[1] Search by Collection ID")
            print("[2] Search by Collection Name")
            sub_choice = input("Choose (1 or 2): ").strip()
            if sub_choice == "1":
                args.collection_id = input("Enter Collection ID: ").strip()
            elif sub_choice == "2":
                args.collection_name = input("Enter Collection Name: ").strip()
        handle_copy_mode(args)

    elif choice == "2":
        url = input("Enter Medal.tv clip URL: ").strip()
        save_dir = (
            input(f"Save downloads where? [Enter for {default_clips_dir}]: ").strip()
            or default_clips_dir
        )
        args = argparse.Namespace(url=url, save_dir=save_dir)
        handle_download_mode(args)
    else:
        print("Invalid choice.")


def main():
    paths = get_default_paths()
    default_clips_dir = paths["default_clips_dir"]
    default_json_path = paths["default_json_path"]

    parser = argparse.ArgumentParser(description="MedalTV CLI")
    subparsers = parser.add_subparsers(dest="command")

    # --- Copy command ---
    copy_parser = subparsers.add_parser("copy", help="Copy local clips")
    copy_parser.add_argument("--json", default=default_json_path)
    copy_parser.add_argument("--copy-dir", default=default_clips_dir)

    group = copy_parser.add_mutually_exclusive_group()
    group.add_argument("--path-text")
    group.add_argument("--title")
    group.add_argument("--collection-id")
    group.add_argument("--collection-name")

    # --- Download command ---
    dl_parser = subparsers.add_parser("download", help="Download clip")
    dl_parser.add_argument("--url", required=True)
    dl_parser.add_argument("--save-dir", default=default_clips_dir)

    args = parser.parse_args()

    # If no command is provided, run interactive
    if not sys.argv[1:]:
        interactive_menu()
    elif args.command == "copy":
        handle_copy_mode(args)
    elif args.command == "download":
        handle_download_mode(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
