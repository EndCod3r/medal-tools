import json
import shutil
import os


def find_clips(json_file_path):
    """Extracts clip file paths from a JSON file"""
    try:
        with open(json_file_path, "r") as file:
            data = json.load(file)

        file_paths = []
        for clip_id, clip_data in data.items():
            if "FilePath" in clip_data:
                file_path = clip_data["FilePath"].strip()
                if file_path:
                    file_paths.append(file_path)
        return file_paths

    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file_path}")
        return []
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return []


def find_clips_by_collection_id(json_file_path, collection_id):
    """Find clips belonging to a specific collection ID"""
    try:
        with open(json_file_path, "r") as file:
            data = json.load(file)

        matching_clips = []
        for clip_id, clip_data in data.items():
            content = clip_data.get("Content", {})
            collections = content.get("contentCollections", [])

            if any(
                collection.get("collectionId") == collection_id
                for collection in collections
            ):
                file_path = clip_data.get("FilePath", "").strip()
                if file_path:
                    matching_clips.append(file_path)

        return matching_clips

    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file_path}")
        return []
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return []


def find_clips_by_collection_name(json_file_path, collection_name):
    """Find clips by collection name (case-insensitive substring match)"""
    try:
        with open(json_file_path, "r") as file:
            data = json.load(file)

        matching_clips = []
        collection_name = collection_name.lower()

        for clip_id, clip_data in data.items():
            content = clip_data.get("Content", {})
            collections = content.get("contentCollections", [])
            names = [c.get("name", "").lower() for c in collections]
            if any(collection_name in name for name in names):
                file_path = clip_data.get("FilePath", "").strip()
                if file_path:
                    matching_clips.append(file_path)

        return matching_clips

    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file_path}")
        return []
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return []


def find_clips_by_path_text(json_file_path, search_string):
    """Find clips by search string in file path"""
    all_clips = find_clips(json_file_path)
    search_string = search_string.lower()
    return [
        clip for clip in all_clips if search_string in os.path.basename(clip).lower()
    ]


def find_clips_by_title(json_file_path, search_string):
    """Find clips by search string in clip title (contentTitle)"""
    search_string = search_string.lower()
    try:
        with open(json_file_path, "r") as file:
            data = json.load(file)

        matching_clips = []
        for clip_data in data.values():
            content_title = clip_data.get("Content", {}).get("contentTitle", "").lower()
            if search_string in content_title:
                file_path = clip_data.get("FilePath", "").strip()
                if file_path:
                    matching_clips.append(file_path)

        return matching_clips
    except Exception as e:
        print(f"Error in find_clips_by_title: {e}")
        return []


def extract_clips(clips_list, target_directory):
    """Copies clips to target directory"""
    os.makedirs(target_directory, exist_ok=True)
    copied_count = 0
    skipped_count = 0

    try:
        for file_path in clips_list:
            file_path = file_path.strip()
            if not file_path:
                continue

            if os.path.exists(file_path):
                file_name = os.path.basename(file_path)
                destination = os.path.join(target_directory, file_name)

                if os.path.exists(destination):
                    print(f"Skipped existing: {file_name}")
                    skipped_count += 1
                else:
                    shutil.copy2(file_path, destination)
                    print(f"Copied: {file_name}")
                    copied_count += 1
            else:
                print(f"Missing file: {file_path}")

        print(
            f"\nOperation complete! Copied {copied_count} files, skipped {skipped_count} files."
        )
        return True

    except Exception as e:
        print(f"Error during copy operation: {str(e)}")
        return False


def filter_clips_by_name(clips_list, search_string):
    """Filter clips list by substring in filename"""
    return [
        clip
        for clip in clips_list
        if search_string.lower() in os.path.basename(clip).lower()
    ]
