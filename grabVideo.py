#!/usr/bin/env python3
import os
import sys

if len(sys.argv) == 2:
	FILE = sys.argv[1]
	try:
		links = open(FILE, "r").readlines()
	except FileNotFoundError:
		print(FILE, " doesn't exist!")
		quit()
	for link in links:
		cmd = "./instagram_video_download.sh "+str(link)
		os.system(cmd)
