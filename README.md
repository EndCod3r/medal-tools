# Medal.TV Tools

I made a very simple PowerShell script that did served this same purpose but everything was hard coded into the script but I needed the ability to copy all of my clips to a different directory for ease of access for my [YouTube videos](https://youtube.com/@EndLordHD). So I decided to re-write it in Python (with the help of AI) and it now works way better!

## Functions:

- Copy clips to directory
  - Copying clips with certain string in path (eg. Game name, date, etc)
  - Copying clips by collectionID (custom albums)
- Download clips from Medal.TV
- Fully function GUI
  - Searching for clips
    - by text in path
    - by text in title
    - by collection name/ID
  - Copying clips
    - by text in path
    - by text in title
    - by collection name/ID
  - Checking for enough disk space to copy clips

### Planned:

- Copying and seraching clips by tags and game category
- Downloading clips through the GUI

## How to download:

### Git Clone:

```
git clone https://github.com/EndCod3r/medal-tools.git
cd medal-tools
```

or if you don't have [Git](https://git-scm.com) installed

### Download Zip:

Look for and click the green `<> Code` button near the top of this repo's page and click `Download ZIP`, and once it's done unzip the archive.

## How to use:

Make sure you have [Python](https://www.python.org/downloads/) installed and make sure to select Add Python to PATH while installing.

Open a terminal in the medal-tools folder and run

```
pip install -r requirements.txt
```

Finally run `python cli.py` for the CLI or `python gui.py` for a GUI.

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

This function requires [yt-dlp](https://github.com/yt-dlp/yt-dlp). Download yt-dlp.exe file from the release page and put it in the same directory as `main.py` or else it will give you an error and wont work. You can download videos from other websites too (eg. YouTube, TikTok, etc.) but for more options when downloading videos you should use [ThioJoe's](https://youtube.com/@ThioJoe) [youtube-dl-easy](https://github.com/ThioJoe/youtube-dl-easy).

The download clip function is heavily inspired by [ThioJoe's](https://youtube.com/@ThioJoe) [youtube-dl-easy](https://github.com/ThioJoe/youtube-dl-easy).
