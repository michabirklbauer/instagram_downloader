#!/usr/bin/env python3

from instaload import instaload, is_private
from tkinter import filedialog
import tkinter as tk
from lxml import html
import urllib.request as ur
import requests
import json
import sys
import os

def pipeline(i_url):
	if is_private(i_url):
		print("It appears you entered a link to a private post, script will try to download anyway!")
		try:
			instaload(i_url)
		except:
			print("Failed to download post! Please try manually!")
	else:
		instaload(i_url)
	print("FINISHED")
	return

def link_list_dl():
	f = filedialog.askopenfilename()
	with open(f, "r") as in_file:
		lines = in_file.readlines()
		in_file.close()
	for line in lines:
		l = line.lstrip().rstrip()
		if is_private(l):
			print("It appears your link list also contains links to private posts, script will try to download anyway but manually checking is advised! Private links will be filtered and appended to private.txt!")
			try:
				instaload(l)
			except:
				pass
			with open("private.txt", "a") as p_file:
				p_file.write(l+"\n")
				p_file.close()
		else:
			instaload(l)
	print("FINISHED")
	return

if __name__ == '__main__':
	root = tk.Tk()
	root.title("Instagram Downloader by Micha")
	#headerFrame with image
	mainImg = tk.PhotoImage(file="main")
	mainFrame = tk.Label(root, image=mainImg)
	mainFrame.image = mainImg
	mainFrame.grid(row=0, column=0, rowspan=4, columnspan=7)
	#titleFrame
	titleFrame = tk.Label(root, text="\nEnter link to post or select a link file:")
	titleFrame.grid(row=4, column=0, columnspan=7)
	link_entry = tk.Entry(root, width=45)
	link_entry.grid(row=5, column=0, columnspan=6)
	link_confirm = tk.Button(root, text="Download!", command= lambda: pipeline(str(link_entry.get())))
	link_confirm.grid(row=5, column=6)
	link_alt = tk.Button(root, text="Choose a link file!", command=link_list_dl)
	link_alt.grid(row=6, column=0, columnspan=7, sticky="N")
	root.mainloop()