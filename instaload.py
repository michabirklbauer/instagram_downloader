#!/usr/bin/env python3

import urllib.request as ur
import json
import sys
import os

def get_image(json_data, prefix=""):
	dimensions_h = int(json_data["dimensions"]["height"])
	dimensions_w = int(json_data["dimensions"]["width"])
	display_resources = json_data["display_resources"]
	image_src = ""
	image_display = ""
	for resource in display_resources:
		if int(resource["config_height"])==dimensions_h and int(resource["config_width"])==dimensions_w:
			image_src = str(resource["src"])
			break
	try:
		image_display = str(json_data["display_url"])
	except:
		print("Error: Failed to extract image from display_url!")
		image_display = ""
	if image_display == image_src:
		image = image_display
	else:
		if image_src == "" and image_display != "":
			print("Warning: image_src and image_display not the same!")
			print("image_src is NULL")
			print("Getting display_url!")
			image = image_display
		elif image_src != "" and image_display == "":
			print("Warning: image_src and image_display not the same!")
			print("image_display is NULL")
			print("Getting display_resources!")
			image = image_src
		else:
			print("Warning: image_src and image_display not the same!")
			print("image_src: \n" + image_src)
			print("image_display: \n" + image_display)
			print("Default: Getting display_url!")
			image = image_display
	if image == "":
		print("Error: Failed to extract image!")
		return [1]
	image_link = image.replace("\\", "")
	try:
		if prefix == "":
			file_name = str(image_link).split("/")[-1].split("?")[0]
		else:
			file_name = prefix + "_" + str(image_link).split("/")[-1].split("?")[0]
		ur.urlretrieve(str(image_link), file_name)
		print("Successfully extracted and downloaded image!")
		return [0, image_link]
	except:
		error_msg = "Error: Failed to extract image from link: " + insta_url
		print(error_msg)
		return [1, image_link]

def get_video(json_data, prefix=""):
	dimensions_h = int(json_data["dimensions"]["height"])
	dimensions_w = int(json_data["dimensions"]["width"])
	display_resources = json_data["display_resources"]
	image_src = ""
	image_display = ""
	result = []
	for resource in display_resources:
		if int(resource["config_height"])==dimensions_h and int(resource["config_width"])==dimensions_w:
			image = str(resource["src"])
			break
	try:
		image_display = str(json_data["display_url"])
	except:
		print("Error: Failed to extract image from display_url!")
		image_display = ""
	if image_display == image_src:
		image = image_display
	else:
		if image_src == "" and image_display != "":
			print("Warning: image_src and image_display not the same!")
			print("image_src is NULL")
			print("Getting display_url!")
			image = image_display
		elif image_src != "" and image_display == "":
			print("Warning: image_src and image_display not the same!")
			print("image_display is NULL")
			print("Getting display_resources!")
			image = image_src
		else:
			print("Warning: image_src and image_display not the same!")
			print("image_src: \n" + image_src)
			print("image_display: \n" + image_display)
			print("Default: Getting display_url!")
			image = image_display
	if image == "":
		print("Error: Failed to extract image!")
		print("Trying to get video!")
	else:
		image_link = image.replace("\\", "")
		try:
			if prefix == "":
				file_name = str(image_link).split("/")[-1].split("?")[0]
			else:
				file_name = prefix + "_" + str(image_link).split("/")[-1].split("?")[0]
			ur.urlretrieve(str(image_link), file_name)
			print("Successfully extracted and downloaded image!")
			result.append(image_link)
		except:
			error_msg = "Error: Failed to extract image from link: " + insta_url
			print(error_msg)
			print("Trying to get video!")
			result.append("no image")
	video = str(json_data["video_url"])
	video_link = video.replace("\\", "")
	try:
		if prefix == "":
			file_name = str(video_link).split("/")[-1].split("?")[0]
		else:
			file_name = prefix + "_" + str(video_link).split("/")[-1].split("?")[0]
		ur.urlretrieve(str(video_link), file_name)
		print("Successfully extracted and downloaded video!")
		result.append(video_link)
		result.insert(0, 0)
		return result
	except:
		error_msg = "Error: Failed to extract video from link: " + insta_url
		print(error_msg)
		result.append(video_link)
		result.insert(0, 1)
		return result

def instaload(insta_url):

	insta_url_api = str(insta_url).rstrip("/") + "/?__a=1"
	data = ur.urlopen(insta_url_api).read()

	try:
		json_data = json.loads(data)
	except:
		print("Error: Failed to load json data!")
		return 1

	if str(json_data["graphql"]["shortcode_media"]["__typename"]) == "GraphImage":
		r = get_image(json_data["graphql"]["shortcode_media"])
		if r[0] == 0:
			return 0
		else:
			return 1
	elif str(json_data["graphql"]["shortcode_media"]["__typename"]) == "GraphVideo":
		prefix = str(json_data["graphql"]["shortcode_media"]["shortcode"])
		r = get_video(json_data["graphql"]["shortcode_media"], prefix)
		if r[0] == 0:
			return 0
		else:
			return 1
	elif str(json_data["graphql"]["shortcode_media"]["__typename"]) == "GraphSidecar":
		prefix = str(json_data["graphql"]["shortcode_media"]["shortcode"])
		edges = json_data["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"]
		r = 0
		for edge in edges:
			if str(edge["node"]["__typename"]) == "GraphImage":
				r_ = get_image(edge["node"], prefix)
			elif str(edge["node"]["__typename"]) == "GraphVideo":
				r_ = get_video(edge["node"], prefix)
			else:
				print("Error: Unrecognized typename!")
				return 1
			if r_[0] == 1:
				r = 1
		return r
	else:
		print("Error: Unrecognized typename!")
		return 1

def is_private(insta_url):
	url = str(insta_url)
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
				r = instaload(i_url)
			except:
				print("Failed to download post! Please try manually!")
		else:
			r = instaload(i_url)
		if r == 0:
			print("Download successfully!")
		else:
			print("Unknown Error encountered: Download may have failed!")
	elif len(sys.argv) == 2:
		if os.path.isfile(sys.argv[1]):
			with open(sys.argv[1], "r") as in_file:
				lines = in_file.readlines()
				in_file.close()
				count = int(len(lines))
				counter = 1
				percent = ["[--------------------]", "[#-------------------]", "[##------------------]", "[###-----------------]", "[####----------------]", "[#####---------------]", "[######--------------]", "[#######-------------]", "[########------------]", "[#########-----------]", "[##########----------]", "[###########---------]", "[############--------]", "[#############-------]", "[##############------]", "[###############-----]", "[################----]", "[#################---]", "[##################--]", "[###################-]", "[####################]"]
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
		else:
			if is_private(sys.argv[1]):
				print("It appears you entered a link to a private post, script will try to download anyway!")
				try:
					r = instaload(sys.argv[1])
				except:
					print("Failed to download post! Please try manually!")
			else:
				r = instaload(sys.argv[1])
			if r == 0:
				print("Download successfully!")
			else:
				print("Unknown Error encountered: Download may have failed!")
	else:
		print("Wrong usage! Try running without parameters or read documentation!")
