# Medal.TV Tools

I made a very simple PowerShell script that did served this same purpose but everything was hard coded into the script but I needed the ability to copy all of my clips to a different directory for ease of access for my [YouTube videos](https://youtube.com/@EndLordHD). So I decided to re-write it in Python (with the help of AI) and it now works way better!

![GUI](https://github.com/user-attachments/assets/04c911c2-0cc3-4ff5-9c7c-2272afeb0d30)

![CLI](https://github.com/user-attachments/assets/aae1c9a2-06b0-4f9a-8eef-3eb3cb2323a6)

> [!WARNING]  
> Make sure you close/restart Medal before copying clips so that the JSON file is saved properly and the script doesn't miss any clips!

## Functions:

- Functional CLI (minimal bugs but less features)

  - Copy clips to a directory
    - Copying clips with a certain string in the path (eg. game name, date, etc)
    - Copying clips from custom albums (collectionId or collection name)
  - Download clips from Medal.TV
  - Supports arguments for one-line copying or downloading

- Mostly functional GUI (some bugs but more features)
  - Searching for clips
    - by text in the path
    - by text in the title
    - by collection name/ID
  - Copying clips
    - by text in the path
    - by text in the title
    - by collection name/ID
  - Checking for enough disk space to copy clips

### Planned:

- Copying and searching clips by tags and game category
- Downloading clips through the GUI

## How to download:

### Git Clone:

```
git clone https://github.com/EndCod3r/medal-tools.git
cd medal-tools
```

or if you don't have [Git](https://git-scm.com) installed

### Download Zip:

Go to the [releases](https://github.com/EndCod3r/medal-tools/releases/latest), and open the Assets drop down, and download the `Source code (zip).` Extract it once it's done.

## How to use:

Ensure you have [Python](https://www.python.org/downloads/) installed and select 'Add Python to PATH' during the installation process.

Open a terminal in the medal-tools folder and run

```
pip install -r requirements.txt
```

Finally, run `python cli.py` for the CLI or `python gui.py` for a GUI.

### Collection IDs:

If you want to copy clips that are in a specific custom album you need the collectionId for that album.

To find it you need to go into your clips.json file.

Open the run dialog box `Win + R` and type `%appdata%\Medal\store` and open `clips.json`

Use `CTRL + F` and type the name of the album you want and before the name of the album will be the collectionId. Copy the collectionId of the album you want to copy and paste it when the script asks for the collection ID!

Example:

```
[{"collectionId":"1d0oPu5MFZv2xJGaFjS","name":"Funny Siege Clips"...}]
```

### Downloading Clips

This function requires [yt-dlp](https://github.com/yt-dlp/yt-dlp). Download yt-dlp.exe file from the releases page and put it in the same directory as `main.py` or else it will give you an error and won't work. You can download videos from other websites too (eg. YouTube, TikTok, etc.) but for more options when downloading videos you should use [ThioJoe's](https://youtube.com/@ThioJoe) [youtube-dl-easy](https://github.com/ThioJoe/youtube-dl-easy).

The download clip function is heavily inspired by [ThioJoe's](https://youtube.com/@ThioJoe) [youtube-dl-easy](https://github.com/ThioJoe/youtube-dl-easy).
