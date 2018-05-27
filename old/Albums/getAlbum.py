#!/usr/bin/env python3
import os

f = open("temporaryInstagramCache.html", "r")
f_content = f.read()

s1 = f_content.split("<body")
s2 = s1[1]

s3 = s2.split("display_url")

i = 0
for frag in s3:
	if i == 0:
		i=i+1
		continue
	elif i == 1:
		i=i+1
		continue
	else:
		s = frag.split("\"")
		cmd = "wget "+s[2]
		os.system(cmd)
