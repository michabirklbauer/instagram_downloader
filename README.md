# instagram_downloader

Scripts written in shell and python to download public pictures, videos and albums from Instagram.

## Requirements
- Python (version 3 or higher) and shell! Sorry to all the Windows users!

## Features
- Download single pictures, videos or albums using the shell scripts (also see "Usage")
- Download multiple pictures, videos or albums by providing a txt file with links to the python scripts
- Filter private links from your txt files, so you can download them manually

## Usage

Example files are included!

- ### Picture download:
  - single pictures:
  ```shell
  ./instagram_download.sh link-to-picture
  ```
  - multiple pictures:
  ```shell
  ./grab.py sample-link-file.txt
  ```
- ### Video download:
  - single videos:
  ```shell
  ./instagram_video_download.sh link-to-video
  ```
  - multiple videos:
  ```shell
  ./grabVideo.py sample-link-video.txt
  ```
- ### Album download:
  - single albums:
  ```shell
  ./instagram_album_download.sh link-to-album (requires getAlbum.py in the same directory)
  ```
  - multiple albums:
  ```shell
  ./grabAlbum.py sample-link-album.txt
  ```
- ### Filter private links from public links for manual download:
  ```shell
  ./privateFilter.py links.txt
  ```
  Will create two files:
  - public.txt: contains all public links (pass this to one of the above scripts!)
  - private.txt: contains all private links (download these manually!)
