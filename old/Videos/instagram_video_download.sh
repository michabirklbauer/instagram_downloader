#!/bin/bash

wget -O temporaryInstagramCache.html $1
cat temporaryInstagramCache.html | grep og:video:secure_url | cut -d'"' -f4 | xargs wget
rm temporaryInstagramCache.html
