# Medal.TV Tools

I already used these because it was way easier to copy files that were in a custom album

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

The download clip function is inspired by [ThioJoe's](https://youtube.com/@ThioJoe) [youtube-dl-easy](https://github.com/ThioJoe/youtube-dl-easy) and requires [youtube-dl](https://yt-dl.org/).
