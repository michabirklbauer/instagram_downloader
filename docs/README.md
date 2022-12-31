# Instagram Downloader by Micha Birklbauer

A python script to download public (and private) pictures, videos and albums from Instagram.

![Screenshot](https://raw.githubusercontent.com/michabirklbauer/instagram_downloader/master/docs/instaload.jpg)

## WARNING

**Instagram deprecated their public API and this repository will not be maintained any longer. Programs/Scripts or parts of them do not work anymore! USE AT OWN RISK!**

## Requirements
- Python (version 3.6 or higher)

## Features
- Download a single picture/video/album by passing the link as a parameter to the script
- Download multiple pictures/videos/albums by passing a file list to the script (as parameter)

## Usage

Examples:

- Download a single post:
  ```shell
  ./instaload.py -url https://www.instagram.com/p/B27CH9qjDFa/
  ```
- **_Recommended:_** Download a single post with specified cookie file:
  ```shell
  ./instaload.py -url https://www.instagram.com/p/B27CH9qjDFa/ -c cookie.txt
  ```
- Download multiple posts using a filelist (e.g. links.txt):
  ```shell
  ./instaload.py -f links.txt
  ```
- **_Recommended:_** Download multiple posts with specified cookie file:
  ```shell
  ./instaload.py -f links.txt -c cookie.txt
  ```

## Why specify a cookie file?

- Instagram will not time out your API requests after downloading a few posts.
- Access to the newer API version with higher resolution pictures.
- Ability to download posts from private profiles that you follow.

## How to get your cookie file

- Open your browser and login to Instagram.
- Open the developer console.
- Go to network and access the Instagram API by loading an Instagram page with postfix "?__a=1" e.g. "https://www.instagram.com/instagram/?__a=1"
- You should see a GET request to "/instagram/?__a=1", click it and go to the request header and copy all the text that is in "Cookie" into a txt file.
- Done!
- (An exemplary cookie file `cookie.txt` is given for illustration purposes.)

## Credits
- Picture: [Unsplash - Lance Asper](https://unsplash.com/photos/3P3NHLZGCp8)
- Font: [Mightype Script](https://www.behance.net/gallery/29992721/Mightype-Script-Free-Handlettered-Font)

## License

[MIT License](https://github.com/michabirklbauer/instagram_downloader/blob/master/LICENSE.md)

## Download
- ZIP: [DOWNLOAD](https://github.com/michabirklbauer/instagram_downloader/archive/master.zip)
- TAR.GZ: [DOWNLOAD](https://github.com/michabirklbauer/instagram_downloader/archive/master.tar.gz)

## Contact
- Website: [michabirklbauer.github.io](https://michabirklbauer.github.io/)
- Contact: [micha.birklbauer@gmail.com](mailto:micha.birklbauer@gmail.com)
