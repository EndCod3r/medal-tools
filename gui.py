import os
import json
import time
import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import filedialog, messagebox, Canvas, Scrollbar, StringVar, END
from PIL import Image, ImageTk
import requests
from io import BytesIO
import threading
from clips_handler import (
    find_clips,
    find_clips_by_collection_id,
    find_clips_by_collection_name,
    find_clips_by_path_text,
    find_clips_by_title,
)
from utils.paths import get_default_paths
import shutil
import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os


class CTkTooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 10
        y = self.widget.winfo_rooty()
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.overrideredirect(True)
        self.tooltip.geometry(f"+{x}+{y}")
        label = tk.Label(
            self.tooltip,
            text=self.text,
            background="#333",
            foreground="white",
            relief="solid",
            borderwidth=1,
            padx=4,
            pady=2,
            font=("Arial", 9),
        )
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


paths = get_default_paths()
default_json_path = paths["default_json_path"]

paths = get_default_paths()
default_json_path = paths["default_json_path"]

cancel_request = False

loaded_clips = []

root = ctk.CTk()
root.title("MedalTV Clip Tool")
root.geometry("1000x650")
root.iconbitmap("assets/icon.ico")

# PanedWindow for two columns
paned = tk.PanedWindow(
    root,
    orient=tk.HORIZONTAL,
    bg="#1D1D1D",
    sashwidth=4,
    sashrelief="flat",
    showhandle=False,
    bd=0,
    relief="flat",
)


paned.pack(fill="both", expand=True)

# Left panel frame (inputs)
left_frame = ctk.CTkFrame(paned, width=300)
paned.add(left_frame, minsize=300)

# Right panel frame (clip list)
right_frame = ctk.CTkFrame(paned)
paned.add(right_frame)

clip_count_var = ctk.StringVar(value="Clips: 0")
clip_count_label = ctk.CTkLabel(
    right_frame, textvariable=clip_count_var, font=("Arial", 14, "bold")
)
clip_count_label.pack(anchor="nw", padx=10, pady=10)


def set_fixed_sash_position():
    paned.sash_place(0, int(root.winfo_width() * 0.4), 0)

    def block_sash_drag(event):
        return "break"

    # Disable sash dragging
    paned.bind("<B1-Motion>", block_sash_drag)


# Wait for the window to be ready, then set sash position and disable drag
root.update_idletasks()
root.after(100, set_fixed_sash_position)

# -------- Left panel inputs --------
ctk.CTkLabel(left_frame, text="JSON File Path:").pack(pady=(10, 0))

json_path_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
json_path_frame.pack(pady=5)

json_path_entry = ctk.CTkEntry(json_path_frame, width=170)
json_path_entry.insert(0, default_json_path)
json_path_entry.pack(side="left", padx=(0, 5))


def browse_json():
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if file_path:
        json_path_entry.delete(0, tk.END)
        json_path_entry.insert(0, file_path)


json_icon_button = ctk.CTkButton(
    json_path_frame,
    text="📂",  # or use an image icon
    width=30,
    height=28,
    command=browse_json,
)
json_icon_button.pack(side="left")
CTkTooltip(json_icon_button, "Browse for JSON")

# Search type dropdown
search_type_var = ctk.StringVar(value="Search Text in Path")
title_text_var = ctk.StringVar()


ctk.CTkLabel(left_frame, text="Select Search Type:").pack(pady=(20, 5))
search_type_menu = ctk.CTkOptionMenu(
    left_frame,
    values=[
        "Search Text in Path",
        "Search Text in Title",
        "Collection Name",
        "Collection ID",
    ],
    variable=search_type_var,
)
search_type_menu.pack(pady=(0, 10))

# Container frame for input widgets
input_container = ctk.CTkFrame(left_frame, fg_color="transparent")
input_container.pack(pady=2)

# Variables
path_text_var = ctk.StringVar()
collection_name_var = ctk.StringVar()
collection_id_var = ctk.StringVar()
title_text_var = ctk.StringVar()


title_label = ctk.CTkLabel(input_container, text="Search Text In Title:")
title_entry = ctk.CTkEntry(input_container, width=200, textvariable=title_text_var)

# Widgets for Search Text in Path
path_label = ctk.CTkLabel(input_container, text="Search Text In Path:")
path_entry = ctk.CTkEntry(input_container, width=200, textvariable=path_text_var)

# Widgets for Collection Name
collection_name_label = ctk.CTkLabel(input_container, text="Collection Name:")
collection_name_entry = ctk.CTkEntry(
    input_container, width=200, textvariable=collection_name_var
)

# Widgets for Collection ID
collection_id_label = ctk.CTkLabel(input_container, text="Collection ID:")
collection_entry = ctk.CTkEntry(
    input_container, width=200, textvariable=collection_id_var
)

# Initially hide all except Search Text widgets
collection_name_label.pack_forget()
collection_name_entry.pack_forget()
collection_id_label.pack_forget()
collection_entry.pack_forget()


def on_search_type_change(choice):
    # Hide all input widgets first
    path_label.pack_forget()
    path_entry.pack_forget()
    title_label.pack_forget()
    title_entry.pack_forget()
    collection_name_label.pack_forget()
    collection_name_entry.pack_forget()
    collection_id_label.pack_forget()
    collection_entry.pack_forget()

    if choice == "Search Text in Path":
        path_label.pack(pady=(10, 0))
        path_entry.pack(pady=(0, 10))
    elif choice == "Search Text in Title":
        title_label.pack(pady=(10, 0))
        title_entry.pack(pady=(0, 10))
    elif choice == "Collection Name":
        collection_name_label.pack(pady=(10, 0))
        collection_name_entry.pack(pady=(0, 10))
    elif choice == "Collection ID":
        collection_id_label.pack(pady=(10, 0))
        collection_entry.pack(pady=(0, 10))


search_type_var.trace_add(
    "write", lambda *args: on_search_type_change(search_type_var.get())
)

# Initialize correct input visible
on_search_type_change(search_type_var.get())


# Enforce mutual exclusivity of inputs
def on_path_text_change(*args):
    if path_text_var.get().strip():
        collection_entry.configure(state="disabled")
    else:
        collection_entry.configure(state="normal")


def on_collection_change(*args):
    if collection_id_var.get().strip():
        path_entry.configure(state="disabled")
    else:
        path_entry.configure(state="normal")


path_text_var.trace_add("write", on_path_text_change)
collection_id_var.trace_add("write", on_collection_change)

# Search Button
ctk.CTkButton(
    left_frame,
    text="Search for Clips",
    command=lambda: threading.Thread(target=lambda: load_clips()).start(),
).pack(pady=20)


# Progress UI (shows under search button)
# Centered frame for loading UI inside left_frame
# Progress UI (centered, hidden initially)
loading_frame = ctk.CTkFrame(left_frame)
loading_frame.place(relx=0.5, rely=0.5, anchor="center")
loading_frame.lower()  # Hide underneath everything initially

# Copy target directory input (below progress bar)
default_copy_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Clips")
os.makedirs(default_copy_path, exist_ok=True)


ctk.CTkLabel(left_frame, text="Copy clips to directory:").pack(pady=(10, 2))
copy_dir_var = ctk.StringVar(value=default_copy_path)
copy_dir_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
copy_dir_frame.pack(pady=(0, 10))


def browse_copy_dir():
    folder = filedialog.askdirectory()
    if folder:
        copy_dir_var.set(folder)


copy_dir_entry = ctk.CTkEntry(copy_dir_frame, width=170, textvariable=copy_dir_var)
copy_dir_entry.pack(side="left", padx=(0, 5))

copy_icon_button = ctk.CTkButton(
    copy_dir_frame,
    text="📁",
    width=30,
    height=28,
    command=browse_copy_dir,
)
copy_icon_button.pack(side="left")
CTkTooltip(copy_icon_button, "Browse for Folder")


def threaded_copy_clips():
    threading.Thread(target=copy_clips_with_progress, daemon=True).start()


# Frame to hold Copy Clips and Check Disk Space buttons side by side
btn_frame = ctk.CTkFrame(left_frame)
btn_frame.pack(pady=(0, 20))

copy_btn = ctk.CTkButton(
    btn_frame,
    text="Copy Clips",
    command=threaded_copy_clips,  # set the command here
    state="normal",  # or "disabled" if you want to start disabled
)
copy_btn.pack(side="left", padx=(0, 10))


# Centered loading UI (initially hidden)
loading_frame = ctk.CTkFrame(
    root,
    fg_color="#1d1d1d",  # slightly darker gray background
    border_width=1,  # border thickness
    border_color="black",  # border color
)
loading_frame.place(relx=0.5, rely=0.45, anchor="center")


progress_var = ctk.StringVar()
progress_label = ctk.CTkLabel(
    loading_frame,
    textvariable=progress_var,
    font=("Arial", 14),
)
progress_label.pack(pady=(10, 5), padx=20)

progress_bar = ctk.CTkProgressBar(loading_frame, width=300)

progress_bar.pack(pady=(0, 10), padx=20)

loading_frame.lower()  # hidden by default

cancel_button = ctk.CTkButton(
    loading_frame, text="Cancel", command=lambda: cancel_search()
)
cancel_button.pack(pady=(0, 10))


def start_indeterminate():
    def run():
        value = 0
        direction = 1
        while getattr(progress_bar, "indeterminate_running", False):
            value += direction * 0.01
            if value >= 1:
                value = 1
                direction = -1
            elif value <= 0:
                value = 0
                direction = 1
            progress_bar.set(value)
            time.sleep(0.02)

    progress_bar.indeterminate_running = True
    threading.Thread(target=run, daemon=True).start()


def enable_inputs():
    path_entry.configure(state="normal")
    collection_name_entry.configure(state="normal")
    collection_entry.configure(state="normal")
    search_type_menu.configure(state="normal")


# Function to stop the indeterminate animation
def stop_indeterminate():
    progress_bar.indeterminate_running = False
    progress_bar.set(0)


def show_loading(message):
    progress_var.set(message)
    loading_frame.lift()
    start_indeterminate()


def hide_loading():
    stop_indeterminate()
    loading_frame.lower()
    progress_var.set("")


def cancel_search():
    global cancel_requested
    cancel_requested = True
    progress_var.set("Cancelling...")


def get_filtered_clips():
    json_path = json_path_entry.get().strip()
    search_type = search_type_var.get()
    filter_text = ""

    if search_type == "Search Text in Path":
        filter_text = path_text_var.get().strip().lower()
        return find_clips_by_path_text(json_path, filter_text)
    elif search_type == "Search Text in Title":
        filter_text = (
            title_text_var.get().strip().lower()
        )  # Add a separate input field for title search
        return find_clips_by_title(json_path, filter_text)
    elif search_type == "Collection Name":
        filter_text = collection_name_var.get().strip().lower()
        return find_clips_by_collection_name(json_path, filter_text)
    elif search_type == "Collection ID":
        filter_text = collection_id_var.get().strip()
        return find_clips_by_collection_id(json_path, filter_text)

    return []


# Check Disk Space button
def check_disk_space():
    target_dir = copy_dir_var.get().strip()
    if not target_dir:
        messagebox.showerror("Error", "Please select a target directory first.")
        return

    clips = get_filtered_clips()
    if not clips:
        messagebox.showerror("Error", "No clips found to check.")
        return

    json_path = json_path_entry.get().strip()
    try:
        with open(json_path, "r") as file:
            data = json.load(file)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load JSON file: {e}")
        return

    total_size = 0
    for path in clips:
        clip_obj = next((v for v in data.values() if v.get("FilePath") == path), None)
        if clip_obj and "Size" in clip_obj:
            total_size += clip_obj["Size"]
        elif os.path.exists(path):
            total_size += os.path.getsize(path)

    try:
        free_space = shutil.disk_usage(target_dir).free
    except Exception as e:
        messagebox.showerror("Error", f"Failed to check disk space: {e}")
        return

    def format_bytes(size_bytes):
        size_mb = size_bytes / (1024**2)
        if size_mb >= 1000:
            return f"{size_mb / 1024:.2f} GB"
        return f"{size_mb:.2f} MB"

    required_str = format_bytes(total_size)
    available_str = format_bytes(free_space)

    if total_size > free_space:
        messagebox.showwarning(
            "Insufficient Disk Space",
            f"Not enough free space to copy clips.\n"
            f"Required: {required_str}\n"
            f"Available: {available_str}",
        )
    else:
        messagebox.showinfo(
            "Disk Space Check",
            f"Enough disk space available.\n"
            f"Required: {required_str}\n"
            f"Available: {available_str}",
        )


check_btn = ctk.CTkButton(btn_frame, text="Check Disk Space", command=check_disk_space)
check_btn.pack(side="left")


def copy_clips():
    target_dir = copy_dir_var.get().strip()
    if not target_dir:
        messagebox.showerror("Error", "Please select a target directory to copy clips.")
        return

    json_path = json_path_entry.get().strip()
    if not os.path.exists(json_path):
        messagebox.showerror("Error", "JSON file not found.")
        return

    try:
        with open(json_path, "r") as file:
            data = json.load(file)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load JSON file: {e}")
        return

    search_type = search_type_var.get()
    filter_text = ""

    if search_type == "Search Text in Path":
        filter_text = path_text_var.get().strip().lower()
    elif search_type == "Collection Name":
        filter_text = collection_name_var.get().strip().lower()
    elif search_type == "Collection ID":
        filter_text = collection_id_var.get().strip()

    # Filter matching clips
    matching_paths = []
    for v in data.values():
        file_path = v.get("FilePath")
        if not file_path:
            continue

        if search_type == "Search Text in Path":
            if filter_text in os.path.basename(file_path).lower():
                matching_paths.append(file_path)

        elif search_type == "Collection Name":
            collections = v.get("Content", {}).get("contentCollections", [])
            names = [c.get("name", "").lower() for c in collections]
            if any(filter_text in name for name in names):
                matching_paths.append(file_path)

        elif search_type == "Collection ID":
            collections = v.get("Content", {}).get("contentCollections", [])
            ids = [c.get("collectionId", "") for c in collections]
            if filter_text in ids:
                matching_paths.append(file_path)

    if not matching_paths:
        messagebox.showinfo("No Clips", "No matching clips found to copy.")
        return

    os.makedirs(target_dir, exist_ok=True)
    copied, skipped, missing = 0, 0, 0

    for clip_path in matching_paths:
        if not clip_path or not os.path.exists(clip_path):
            missing += 1
            continue
        file_name = os.path.basename(clip_path)
        dest = os.path.join(target_dir, file_name)
        if os.path.exists(dest):
            skipped += 1
            continue
        try:
            import shutil

            shutil.copy2(clip_path, dest)
            copied += 1
        except Exception as e:
            print(f"Failed to copy {file_name}: {e}")

    messagebox.showinfo(
        "Copy Completed",
        f"Copied: {copied} files\nSkipped (already exist): {skipped}\nMissing files: {missing}",
    )


# -------- Right panel clip list --------
canvas = tk.Canvas(right_frame, bg="#333333", highlightthickness=0)
scrollbar = ctk.CTkScrollbar(right_frame, orientation="vertical", command=canvas.yview)
scroll_frame = ctk.CTkFrame(right_frame)


def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.itemconfig(scroll_frame_id, width=canvas.winfo_width())


scroll_frame_id = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
scroll_frame.bind("<Configure>", on_frame_configure)
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Placeholder image for thumbnails (gray)
placeholder_pil = Image.new("RGB", (160, 90), "gray")
placeholder_image = CTkImage(
    light_image=placeholder_pil, dark_image=placeholder_pil, size=(160, 90)
)

# Keep references to thumbnail images to avoid garbage collection
thumb_images = {}


from customtkinter import CTkImage  # put this at the top with other imports


def download_and_set_thumbnail(clip_id, url, label):
    try:
        if url:
            if "thumbnail144p" not in url:
                if "thumbnail1080p" in url:
                    url = url.replace("thumbnail1080p", "thumbnail144p")
                else:
                    url = url.split("?")[0]
                    url += "?width=256"

            response = requests.get(url, timeout=4)
            img_data = response.content
            pil_img = Image.open(BytesIO(img_data)).resize((160, 90))
            img = CTkImage(
                light_image=pil_img, dark_image=pil_img, size=(160, 90)
            )  # <-- Use CTkImage here

            def update_label():
                label.configure(image=img)
                thumb_images[clip_id] = img  # keep reference

            root.after(0, update_label)
    except Exception:
        pass  # keep placeholder if fail


def clear_clips():
    for widget in scroll_frame.winfo_children():
        widget.destroy()
    thumb_images.clear()


copy_btn = ctk.CTkButton(btn_frame, text="Copy Clips", state="normal")
copy_btn.pack(side="left", padx=(0, 10))


# Update `load_clips()` to show loading bar while searching
def load_clips():
    global loaded_clips, cancel_requested
    cancel_requested = False  # Reset at the start

    json_path = json_path_entry.get().strip()
    if not os.path.exists(json_path):
        messagebox.showerror("Error", "JSON file not found.")
        return

    # Disable inputs during search
    path_entry.configure(state="disabled")
    collection_name_entry.configure(state="disabled")
    collection_entry.configure(state="disabled")
    search_type_menu.configure(state="disabled")
    show_loading("Searching for clips...")

    clear_clips()

    try:
        with open(json_path, "r") as file:
            data = json.load(file)

        clips = get_filtered_clips()

        if cancel_requested:
            enable_inputs()
            hide_loading()
            return

        if not clips:
            messagebox.showinfo("No Clips", "No matching clips found.")
            enable_inputs()
            hide_loading()
            return

        loaded_clips = clips
        copy_btn.configure(state="normal")

        for clip_path in loaded_clips:
            if cancel_requested:
                break
            create_clip_row(clip_path, data)

        if not cancel_requested:
            clip_count_var.set(f"Clips: {len(loaded_clips)}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load clips: {e}")
    finally:
        enable_inputs()
        hide_loading()


def create_clip_row(clip_path, data):
    clip_obj = next((v for v in data.values() if v.get("FilePath") == clip_path), None)
    if not clip_obj:
        return

    def open_clip(path):
        if sys.platform.startswith("darwin"):
            subprocess.call(("open", path))
        elif os.name == "nt":  # Windows
            os.startfile(path)
        elif os.name == "posix":  # Linux
            subprocess.call(("xdg-open", path))

    content = clip_obj.get("Content", {})
    clip_name = content.get("contentTitle", "Untitled")
    duration = round(clip_obj.get("duration", 0))
    collections = content.get("contentCollections", [])
    collection_names = (
        ", ".join(c.get("name", "No Name") for c in collections)
        if collections
        else "No Collection"
    )
    timestamp = clip_obj.get("TimeCreated", None)
    date_str = (
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        if timestamp
        else "Unknown Date"
    )

    local_thumb_path = clip_obj.get("Image", None)

    row = ctk.CTkFrame(scroll_frame, width=570, height=110)
    row.pack(fill="x", anchor="e")
    row.pack_propagate(False)

    thumb_frame = ctk.CTkFrame(row, width=160, height=90)
    thumb_frame.pack_propagate(False)
    thumb_frame.pack(side="left", padx=8, pady=10)

    use_online_thumb = False

    if local_thumb_path:
        try:
            pil_img = Image.open(local_thumb_path)
            pil_img = pil_img.resize((160, 90), Image.LANCZOS)
            ctk_img = ctk.CTkImage(
                light_image=pil_img, dark_image=pil_img, size=(160, 90)
            )
        except Exception as e:
            print(f"Failed loading local thumbnail: {e}")
            ctk_img = placeholder_image
            use_online_thumb = True
    else:
        ctk_img = placeholder_image
        use_online_thumb = True

    thumb_label = ctk.CTkLabel(thumb_frame, image=ctk_img, text="")
    thumb_label.pack(fill="both", expand=True)
    thumb_label.configure(cursor="hand2")

    minutes = duration // 60
    seconds = duration % 60
    duration_str = f"{minutes:02}:{seconds:02}"

    info = ctk.CTkFrame(row)
    info.pack(side="left", fill="both", expand=True, padx=(0, 8), pady=10)
    # No fixed width here, so it expands with the window
    info.pack_propagate(True)

    thumb_label.bind("<Button-1>", lambda e: open_clip(clip_path))
    # For clip name label, assuming you assign it to a variable 'clip_name_label':
    clip_name_label = ctk.CTkLabel(
        info,
        text=clip_name,
        font=("Arial", 13, "bold"),
        text_color="white",
        wraplength=380,
        justify="left",
    )
    clip_name_label.pack(anchor="w", pady=(2, 0), fill="x")
    clip_name_label.configure(cursor="hand2")

    clip_name_label.bind("<Button-1>", lambda e: open_clip(clip_path))

    ctk.CTkLabel(
        info,
        text=f"Collections: {collection_names}",
        font=("Arial", 11),
        text_color="white",
    ).pack(anchor="w", pady=(0, 3))

    bottom_frame = ctk.CTkFrame(info, fg_color="transparent", border_width=0)
    bottom_frame.pack(fill="x", pady=(3, 0))

    ctk.CTkLabel(
        bottom_frame,
        text=f"Captured: {date_str}",
        font=("Arial", 10),
        text_color="white",
        fg_color="transparent",
        corner_radius=0,
        padx=0,
        pady=0,
    ).pack(side="left")

    dur_label = ctk.CTkLabel(
        bottom_frame,
        text=duration_str,
        font=("Arial", 12, "bold"),
        text_color="white",
        fg_color="transparent",
        corner_radius=0,
        padx=8,
        pady=0,
    )
    dur_label.pack(side="right")

    thumb_url = (
        clip_obj.get("thumbnail144p")
        or clip_obj.get("thumbnailURL")
        or content.get("thumbnail144p")
        or content.get("thumbnailUrl")
    )
    if not use_online_thumb and thumb_url:
        threading.Thread(
            target=download_and_set_thumbnail,
            args=(clip_path, thumb_url, thumb_label),
            daemon=True,
        ).start()


# Update copy_clips() to check disk space & show progress
def copy_clips_with_progress():
    target_dir = copy_dir_var.get().strip()
    if not target_dir:
        messagebox.showerror("Error", "Please select a target directory to copy clips.")
        return

    json_path = json_path_entry.get().strip()
    if not os.path.exists(json_path):
        messagebox.showerror("Error", "JSON file not found.")
        return

    # Determine which clips to copy
    clips = get_filtered_clips()
    if not clips:
        messagebox.showinfo("No Clips", "No matching clips found to copy.")
        return

    os.makedirs(target_dir, exist_ok=True)

    total = len(clips)
    copied, skipped, missing = 0, 0, 0

    def update_progress(text, progress):
        progress_var.set(text)
        progress_bar.set(progress)

    root.after(0, lambda: show_loading("Copying clips..."))
    for idx, clip_path in enumerate(clips):
        if not clip_path or not os.path.exists(clip_path):
            missing += 1
        else:
            file_name = os.path.basename(clip_path)
            dest = os.path.join(target_dir, file_name)
            if os.path.exists(dest):
                skipped += 1
            else:
                try:
                    shutil.copy2(clip_path, dest)
                    copied += 1
                except Exception as e:
                    print(f"Failed to copy {file_name}: {e}")

        progress_text = f"Copying {idx + 1}/{total}..."
        root.after(0, update_progress, progress_text, (idx + 1) / total)

    root.after(0, hide_loading)
    messagebox.showinfo(
        "Copy Completed",
        f"Copied: {copied} files\nSkipped (already exist): {skipped}\nMissing files: {missing}",
    )


root.mainloop()
