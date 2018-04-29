# instagram_downloader
A simple bash script to do download instagram pictures

works as the following: ./instagram_download.sh link-to-picture e.g. ./instagram_download.sh https://www.instagram.com/p/BPB61smjfNe

10.03.2017

added a python script for using with a txt-file having multiple links to download several pictures at once

29.04.2018

added python and bash scripts to download albums and videos

Usage:

Picture download:

./instagram_download.sh link-to-picture
./grab.py sample-link-file.txt

Video download:

./instagram_video_download.sh link-to-video
./grabVideo.py sample-link-video.txt

Album download:

./instagram_album_download.sh link-to-album (requires getAlbum.py in the same directory)
./grabAlbum.py sample-link-album.txt

Filter private links from public links for manual download:

./privateFilter.py links.txt
