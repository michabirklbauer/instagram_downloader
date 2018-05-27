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
		ur.urlretrieve(str(image[0]), str(image[0]).split("/")[-1])
	elif str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["__typename"]) == "GraphVideo":
		video = tree.xpath('//meta[@property="og:video:secure_url"]/@content')
		ur.urlretrieve(str(video[0]), str(video[0]).split("/")[-1])
	elif str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["__typename"]) == "GraphSidecar":
		prefix = str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["shortcode"])
		edges = json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"]
		for edge in edges:
			if edge["node"]["is_video"]:
				url = str(edge["node"]["video_url"])
				ur.urlretrieve(url, prefix+"_"+(url.split("/")[-1]))
			else:
				url = str(edge["node"]["display_url"])
				ur.urlretrieve(url, prefix+"_"+(url.split("/")[-1]))
	else:
		print("Unrecognized typename!")
		
if __name__ == '__main__':
	if len(sys.argv) == 1:
		i_url = input("Please enter an URL to an instagram post e. g. https://www.instagram.com/p/BVKTcWWhyaS/ \n")
		instaload(i_url)
	elif len(sys.argv) == 2:
		if os.path.isfile(sys.argv[1]):
			with open(sys.argv[1], "r") as in_file:
				lines = in_file.readlines()
				in_file.close()
				for line in lines:
					instaload(line.lstrip().rstrip())
		else:
			instaload(sys.argv[1])
	else:
		print("Wrong usage! Try running without parameters or read documentation!")