# Medal.TV Tools

I made a very simple PowerShell script that did served this same purpose but everything was hard coded into the script and I needed the ability to copy all of my clips to a different directory for ease of access for my [YouTube videos](https://youtube.com/@EndLordHD)! So I decided to re-write it in Python (with the help of AI) and it now works way better!

Functions:

- Copy clips to directory
  - Copying clips with certain string in path
  - Copying clips by collectionID (custom albums)
- Download clips from Medal.TV

### Collection IDs

If you want to copy clips that are in a custom album you need the collectionId for that album.

To find it you need to go into your clips.json file.

Open the run dialog box `Win + R` and type `%appdata%\Medal\store` and open `clips.json`

Use `CTRL + F` and tyle `collectionId` and below each collectionId will be the name of the album. Copy the collectionId of the album you want to copy and paste it when the script asks for the collection ID!

### Downloading Clips

This function required [yt-dlp](https://github.com/yt-dlp/yt-dlp). Download yt-dlp.exe file from the release page and put it in the same directory as `main.py` or else it will give you an error and wont work. You can download clips from other websites too (eg. YouTube, TikTok, etc.) but for more options when downloading videos you should use [ThioJoe's](https://youtube.com/@ThioJoe) [youtube-dl-easy](https://github.com/ThioJoe/youtube-dl-easy).

The download clip function is heavily inspired by [ThioJoe's](https://youtube.com/@ThioJoe) [youtube-dl-easy](https://github.com/ThioJoe/youtube-dl-easy).
