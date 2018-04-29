#!/usr/bin/env python3
import os
import sys

private = open("private.txt", "a")
public = open("public.txt", "a")

if len(sys.argv) == 2:
	FILE = sys.argv[1]
	try:
		links = open(FILE, "r").readlines()
	except FileNotFoundError:
		print(FILE, " doesn't exist!")
		quit()
	for link in links:
		t_1 = link.split("/")
		t_2 = t_1[4]
		if len(t_2) > 12:
			private.write(link)
		else:
			public.write(link)
