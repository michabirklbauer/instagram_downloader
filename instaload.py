#!/usr/bin/env python3

from lxml import html
import urllib.request as ur
import requests
import json
import sys
import os

def instaload(insta_url):
	page = requests.get(insta_url)
	tree = html.fromstring(page.content)
	data = tree.xpath('//body/script[@type="text/javascript"]')

	json_unprocessed = data[0].text_content()
	json_processed = str(json_unprocessed).replace("window._sharedData = ", "").rstrip(";")
	json_data = json.loads(json_processed)

	if str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["__typename"]) == "GraphImage":
		image = tree.xpath('//meta[@property="og:image"]/@content')
		try:
			ur.urlretrieve(str(image[0]), str(image[0]).split("/")[-1].split("?")[0])
		except:
			error_msg = "Error in link: " + insta_url
			print(error_msg)
	elif str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["__typename"]) == "GraphVideo":
		video = tree.xpath('//meta[@property="og:video:secure_url"]/@content')
		try:
			ur.urlretrieve(str(video[0]), str(video[0]).split("/")[-1].split("?")[0])
		except:
			error_msg = "Error in link: " + insta_url
			print(error_msg)
	elif str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["__typename"]) == "GraphSidecar":
		prefix = str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["shortcode"])
		edges = json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"]
		for edge in edges:
			if edge["node"]["is_video"]:
				url = str(edge["node"]["video_url"])
				try:
					ur.urlretrieve(url, prefix+"_"+(url.split("/")[-1].split("?")[0]))
				except:
					error_msg = "Error in link: " + insta_url
					print(error_msg)
			else:
				url = str(edge["node"]["display_url"])
				try:
					ur.urlretrieve(url, prefix+"_"+(url.split("/")[-1].split("?")[0]))
				except:
					error_msg = "Error in link: " + insta_url
					print(error_msg)
	else:
		print("Unrecognized typename!")

def is_private(link):
	url = str(link)
	shortcode = str(url.split("instagram.com/p/")[1]).split("/")[0]
	if len(shortcode) > 12:
		return True
	else:
		return False

if __name__ == '__main__':
	if len(sys.argv) == 1:
		i_url = input("Please enter an URL to an instagram post e. g. https://www.instagram.com/p/BVKTcWWhyaS/ \n")
		if is_private(i_url):
			print("It appears you entered a link to a private post, script will try to download anyway!")
			try:
				instaload(i_url)
			except:
				print("Failed to download post! Please try manually!")
		else:
			instaload(i_url)
	elif len(sys.argv) == 2:
		if os.path.isfile(sys.argv[1]):
			with open(sys.argv[1], "r") as in_file:
				lines = in_file.readlines()
				in_file.close()
				count = int(len(lines))
				counter = 1
				percent = ["[--------------------]", "[#-------------------]", "[##------------------]", "[###-----------------]", "[####----------------]", "[#####---------------]", "[######--------------]", "[#######-------------]", "[########------------]", "[#########-----------]", "[##########----------]", "[###########---------]", "[############--------]", "[#############-------]", "[##############------]", "[###############-----]", "[################----]", "[#################---]", "[##################--]", "[###################-]", "[####################]"]
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
		else:
			if is_private(sys.argv[1]):
				print("It appears you entered a link to a private post, script will try to download anyway!")
				try:
					instaload(sys.argv[1])
				except:
					print("Failed to download post! Please try manually!")
			else:
				instaload(sys.argv[1])
	else:
		print("Wrong usage! Try running without parameters or read documentation!")
