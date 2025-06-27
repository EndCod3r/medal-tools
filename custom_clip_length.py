import json
import os
from utils.paths import get_default_paths

CONFIG_PATH = get_default_paths()["default_config_path"]


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def add_clip_hotkey(config, hotkey, length):
    action = f"clip;length={length}"
    new_entry = {
        "action": action,
        "device": "keyboard",
        "type": "short_press",
        "inputs": hotkey,
    }

    config["recorder"]["triggerHotkeys"].append(new_entry)
    print(f"✅ Added hotkey '{hotkey}' for {length} second clip.")


def main():
    if not os.path.exists(CONFIG_PATH):
        print(f"❌ Config file not found: {CONFIG_PATH}")
        return

    config = load_config(CONFIG_PATH)

    hotkey = input("Enter hotkey (e.g. F6, page down, home): ").strip()
    length = input("Enter clip length in seconds (e.g. 45): ").strip()

    if not length.isdigit():
        print("❌ Invalid length.")
        return

    add_clip_hotkey(config, hotkey, int(length))
    save_config(CONFIG_PATH, config)
    print("✅ Config updated and saved.")


if __name__ == "__main__":
    main()
