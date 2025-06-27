import os


def get_default_paths():
    """Returns default paths configuration"""
    # Get project root directory
    utils_dir = os.path.dirname(os.path.abspath(__file__))
    script_dir = os.path.dirname(utils_dir)  # Go up one level from utils

    return {
        "script_dir": script_dir,
        "default_clips_dir": os.path.join(script_dir, "Clips"),
        "default_json_path": os.path.join(
            os.environ.get("APPDATA", ""), "Medal", "store", "clips.json"
        ),
        "default_config_path": os.path.join(
            os.environ.get("APPDATA", ""), "Medal", "store", "settings.json"
        ),
    }
