#!/bin/bash

getDirName() {
    echo $1 | cut -d '/' -f 5 | xargs basename
}

dir_name=$(getDirName $1)
mkdir $dir_name
cd $dir_name
wget -O temporaryInstagramCache.html $1
cp ../getAlbum.py .
./getAlbum.py
rm getAlbum.py
rm temporaryInstagramCache.html
