#!/bin/bash

wget -O temporaryInstagramCache.html $1
cat temporaryInstagramCache.html | grep og:image | cut -d'"' -f4 | xargs wget
rm temporaryInstagramCache.html
