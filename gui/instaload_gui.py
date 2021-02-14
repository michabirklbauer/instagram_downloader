#!/usr/bin/env python3

# INSTAGRAM DOWNLOADER GUI
# 2021 (c) Micha Johannes Birklbauer
# https://github.com/t0xic-m/
# micha.birklbauer@gmail.com

from instaload import instaload, get_image, get_video, is_private
from tkinter import filedialog
import tkinter as tk
import urllib.request as ur
import json
import os

def download(type, arg):
	if type == 1:
		i_url = input("Please enter an URL to an instagram post e. g. https://www.instagram.com/p/BVKTcWWhyaS/ \n")
		if is_private(i_url):
			print("It appears you entered a link to a private post, script will try to download anyway!")
			try:
				r = instaload(i_url)
			except:
				print("Failed to download post! Please try manually!")
		else:
			r = instaload(i_url)
		if r == 0:
			print("Download successfully!")
		else:
			print("Unknown Error encountered: Download may have failed!")
	elif type == 2:
		if os.path.isfile(arg):
			with open(arg, "r") as in_file:
				lines = in_file.readlines()
				in_file.close()
			count = int(len(lines))
			counter = 1
			percent = [ \
			"[--------------------]", "[#-------------------]",
			"[##------------------]", "[###-----------------]",
			"[####----------------]", "[#####---------------]",
			"[######--------------]", "[#######-------------]",
			"[########------------]", "[#########-----------]",
			"[##########----------]", "[###########---------]",
			"[############--------]", "[#############-------]",
			"[##############------]", "[###############-----]",
			"[################----]", "[#################---]",
			"[##################--]", "[###################-]",
			"[####################]"]
			r = 0
			for line in lines:
				l = line.lstrip().rstrip()
				if is_private(l):
					print("It appears your link list also contains links to private posts, script will try to download anyway but manually checking is advised! Private links will be filtered and appended to private.txt!")
					try:
						r_ = instaload(l)
					except:
						pass
					with open("private.txt", "a") as p_file:
						p_file.write(l+"\n")
						p_file.close()
				else:
					r_ = instaload(l)
				status = counter/count
				status_bar = ""
				if status == 1:
					status_bar = percent[20]
				elif status > 0.95:
					status_bar = percent[19]
				elif status > 0.9:
					status_bar = percent[18]
				elif status > 0.85:
					status_bar = percent[17]
				elif status > 0.8:
					status_bar = percent[16]
				elif status > 0.75:
					status_bar = percent[15]
				elif status > 0.7:
					status_bar = percent[14]
				elif status > 0.65:
					status_bar = percent[13]
				elif status > 0.6:
					status_bar = percent[12]
				elif status > 0.55:
					status_bar = percent[11]
				elif status > 0.5:
					status_bar = percent[10]
				elif status > 0.45:
					status_bar = percent[9]
				elif status > 0.4:
					status_bar = percent[8]
				elif status > 0.35:
					status_bar = percent[7]
				elif status > 0.3:
					status_bar = percent[6]
				elif status > 0.25:
					status_bar = percent[5]
				elif status > 0.2:
					status_bar = percent[4]
				elif status > 0.15:
					status_bar = percent[3]
				elif status > 0.1:
					status_bar = percent[2]
				elif status > 0.05:
					status_bar = percent[1]
				else:
					status_bar = percent[0]
				status_msg = "Downloaded " + str(line) + "\nDownload at " + str(status*100) + "%\n" + status_bar + "\n"
				counter = counter + 1
				print(status_msg)
				if r_ == 1:
					r = 1
			if r == 0:
				print("Downloaded all Posts successfully!")
			else:
				print("Unknown Error encountered: Downloads of one or more Posts may have failed!")
	elif type == 3:
		if is_private(arg):
			print("It appears you entered a link to a private post, script will try to download anyway!")
			try:
				r = instaload(arg)
			except:
				print("Failed to download post! Please try manually!")
		else:
			r = instaload(arg)
		if r == 0:
			print("Download successfully!")
		else:
			print("Unknown Error encountered: Download may have failed!")
	else:
		print("Wrong usage! Try running without parameters or read documentation!")
	return

def link_list_dl():
	f = filedialog.askopenfilename()
	download(2,f)
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
	link_confirm = tk.Button(root, text="Download!", command= lambda: download(3,str(link_entry.get())))
	link_confirm.grid(row=5, column=6)
	link_alt = tk.Button(root, text="Choose a link file!", command=link_list_dl)
	link_alt.grid(row=6, column=0, columnspan=7, sticky="N")
	root.mainloop()
