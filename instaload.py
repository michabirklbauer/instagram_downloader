#!/usr/bin/env python3

# INSTAGRAM DOWNLOADER
# 2022 (c) Micha Johannes Birklbauer
# https://github.com/michabirklbauer/
# micha.birklbauer@gmail.com


import json
import argparse
import urllib.request as ur

class ParseERROR(RuntimeError):
    """
    -- DESCRIPTION --
    Raised if URL could not be parsed properly.
    """
    pass

def get_image(json_data, insta_url, prefix = ""):

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
        print("ERROR: Failed to extract image from display_url!")
        image_display = ""

    if image_display == image_src:
        image = image_display
    else:
        if image_src == "" and image_display != "":
            print("WARNING: image_src and image_display not the same!")
            print("image_src is NULL")
            print("Getting display_url!")
            image = image_display
        elif image_src != "" and image_display == "":
            print("WARNING: image_src and image_display not the same!")
            print("image_display is NULL")
            print("Getting display_resources!")
            image = image_src
        else:
            print("WARNING: image_src and image_display not the same!")
            print("image_src: \n" + image_src)
            print("image_display: \n" + image_display)
            print("Default: Getting display_url!")
            image = image_display

    if image == "":
        error_msg = "ERROR: Failed to extract image from link: " + insta_url
        print(error_msg)
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
        error_msg = "ERROR: Failed to extract image from link: " + insta_url
        print(error_msg)
        return [1, image_link]

def get_image2(json_data, insta_url, prefix = ""):

    image_url = ""
    width = int(json_data["original_width"])
    height = int(json_data["original_height"])
    max_height = 0

    try:
        if "additional_candidates" in json_data["image_versions2"]:
            if "igtv_first_frame" in json_data["image_versions2"]["additional_candidates"]:
                ff_igtv = json_data["image_versions2"]["additional_candidates"]["igtv_first_frame"]["url"]
                if prefix == "":
                    file_name = str(ff_igtv).split("/")[-1].split("?")[0].split(".")[0] + "_ff_igtv.jpg"
                else:
                    file_name = prefix + "_" + str(ff_igtv).split("/")[-1].split("?")[0].split(".")[0] + "_ff_igtv.jpg"
                ur.urlretrieve(str(ff_igtv), file_name)
            if "first_frame" in json_data["image_versions2"]["additional_candidates"]:
                ff = json_data["image_versions2"]["additional_candidates"]["first_frame"]["url"]
                if prefix == "":
                    file_name = str(ff).split("/")[-1].split("?")[0].split(".")[0] + "_ff.jpg"
                else:
                    file_name = prefix + "_" + str(ff).split("/")[-1].split("?")[0].split(".")[0] + "_ff.jpg"
                ur.urlretrieve(str(ff), file_name)
    except:
        print("INFO: Couldn't find any additional image candidates for post: " + insta_url)

    for candidate in json_data["image_versions2"]["candidates"]:
        if int(candidate["height"]) > max_height:
            max_height = int(candidate["height"])
        if int(candidate["width"]) == width and int(candidate["height"]) == height:
            image_url = str(candidate["url"])
            break

    if image_url == "":
        error_msg = "WARNING: Failed to extract image with original_width and original_height\n"
        error_msg += "from link: " + insta_url + "\n"
        error_msg += "tyring to get highest available resolution instead..."
        print(error_msg)
        for candidate in json_data["image_versions2"]["candidates"]:
            if int(candidate["height"]) == max_height:
                image_url = str(candidate["url"])
                break
        if image_url == "":
            error_msg = "ERROR: Failed to extract image from link: " + insta_url
            print(error_msg)
            return [1]

    try:
        if prefix == "":
            file_name = str(image_url).split("/")[-1].split("?")[0]
        else:
            file_name = prefix + "_" + str(image_url).split("/")[-1].split("?")[0]
        ur.urlretrieve(image_url, file_name)
        print("Successfully extracted and downloaded image!")
        return [0, image_url]
    except:
        error_msg = "ERROR: Failed to extract image from link: " + insta_url
        print(error_msg)
        return [1, image_url]

def get_video(json_data, insta_url, prefix = ""):

    dimensions_h = int(json_data["dimensions"]["height"])
    dimensions_w = int(json_data["dimensions"]["width"])
    display_resources = json_data["display_resources"]
    image_src = ""
    image_display = ""
    result = []

    for resource in display_resources:
        if int(resource["config_height"])==dimensions_h and int(resource["config_width"])==dimensions_w:
            image_src = str(resource["src"])
            break

    try:
        image_display = str(json_data["display_url"])
    except:
        print("ERROR: Failed to extract image from display_url!")
        image_display = ""

    if image_display == image_src:
        image = image_display
    else:
        if image_src == "" and image_display != "":
            print("WARNING: image_src and image_display not the same!")
            print("image_src is NULL")
            print("Getting display_url!")
            image = image_display
        elif image_src != "" and image_display == "":
            print("WARNING: image_src and image_display not the same!")
            print("image_display is NULL")
            print("Getting display_resources!")
            image = image_src
        else:
            print("WARNING: image_src and image_display not the same!")
            print("image_src: \n" + image_src)
            print("image_display: \n" + image_display)
            print("Default: Getting display_url!")
            image = image_display

    if image == "":
        error_msg = "ERROR: Failed to extract image from link: " + insta_url
        print(error_msg)
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
            error_msg = "ERROR: Failed to extract image from link: " + insta_url
            print(error_msg)
            print("Trying to get video!")
            result.append(None)

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
        error_msg = "ERROR: Failed to extract video from link: " + insta_url
        print(error_msg)
        result.append(video_link)
        result.insert(0, 1)
        return result

def get_video2(json_data, insta_url, prefix = ""):

    video_url = ""
    width = int(json_data["original_width"])
    height = int(json_data["original_height"])
    max_height = 0

    for candidate in json_data["video_versions"]:
        if int(candidate["height"]) > max_height:
            max_height = int(candidate["height"])
        if int(candidate["width"]) == width and int(candidate["height"]) == height:
            video_url = str(candidate["url"])
            break

    if video_url == "":
        error_msg = "WARNING: Failed to extract video with original_width and original_height\n"
        error_msg += "from link: " + insta_url + "\n"
        error_msg += "tyring to get highest available resolution instead..."
        print(error_msg)
        for candidate in json_data["video_versions"]:
            if int(candidate["height"]) == max_height:
                video_url = str(candidate["url"])
                break
        if video_url == "":
            error_msg = "ERROR: Failed to extract video from link: " + insta_url
            print(error_msg)
            return [1]

    try:
        if prefix == "":
            file_name = str(video_url).split("/")[-1].split("?")[0]
        else:
            file_name = prefix + "_" + str(video_url).split("/")[-1].split("?")[0]
        ur.urlretrieve(video_url, file_name)
        print("Successfully extracted and downloaded video!")
        return [0, video_url]
    except:
        error_msg = "ERROR: Failed to extract video from link: " + insta_url
        print(error_msg)
        return [1, video_url]

def fetch_json_legacy(insta_url):

    request_header = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0" }
    request = ur.Request(insta_url, headers = request_header)
    data = ur.urlopen(request).read()
    data_1 = data.decode("utf-8").split("<script type=\"text/javascript\">window._sharedData = ")[1]
    data_2 = data_1.split(";</script>")[0]
    json_data = json.loads(data_2)
    graphql = json_data["entry_data"]["PostPage"][0]
    if "graphql" not in graphql:
        raise ParseERROR("Couldn't fetch old API data, try using instaload v2.0.0+ with a cookie file!")
    else:
        return graphql

def instaload(insta_url):

    insta_url_api = str(insta_url).rstrip("/") + "/?__a=1"
    request_header = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0" }
    request = ur.Request(insta_url_api, headers = request_header)
    data = ur.urlopen(request).read()

    try:
        json_data = json.loads(data)
    except:
        try:
            json_data = fetch_json_legacy(insta_url)
        except:
            print("ERROR: Failed to load json data!")
            return 1

    if str(json_data["graphql"]["shortcode_media"]["__typename"]) == "GraphImage":
        r = get_image(json_data["graphql"]["shortcode_media"], insta_url)
        if r[0] == 0:
            return 0
        else:
            return 1
    elif str(json_data["graphql"]["shortcode_media"]["__typename"]) == "GraphVideo":
        prefix = str(json_data["graphql"]["shortcode_media"]["shortcode"])
        r = get_video(json_data["graphql"]["shortcode_media"], insta_url, prefix)
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
                r_ = get_image(edge["node"], insta_url, prefix)
            elif str(edge["node"]["__typename"]) == "GraphVideo":
                r_ = get_video(edge["node"], insta_url, prefix)
            else:
                print("ERROR: Unrecognized typename!")
                return 1
            if r_[0] == 1:
                r = 1
        return r
    else:
        print("ERROR: Unrecognized typename!")
        return 1

def instaload2(insta_url, cookie):

    status = 0

    insta_url_api = str(insta_url).rstrip("/") + "/?__a=1"
    request_header = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
                       "Cookie": cookie}
    request = ur.Request(insta_url_api, headers = request_header)
    data = ur.urlopen(request).read()

    try:
        json_data = json.loads(data)
    except:
        print("ERROR: Failed to load json data! Trying to use instaload v1.0.3 instead...")
        return instaload(insta_url)

    if "items" in json_data:
        for item in json_data["items"]:
            if "image_versions2" in item:
                status += get_image2(item, insta_url, str(item["code"]))[0]
            if "video_versions" in item:
                status += get_video2(item, insta_url, str(item["code"]))[0]
            if "carousel_media" in item:
                for carousel_item in item["carousel_media"]:
                    if "image_versions2" in carousel_item:
                        status += get_image2(carousel_item, insta_url, str(item["code"]))[0]
                    if "video_versions" in carousel_item:
                        status += get_video2(carousel_item, insta_url, str(item["code"]))[0]
    else:
        print("INFO: Couldn't fetch new API data, using instaload v1.0.3 instead...")
        return instaload(insta_url)

    return status

def download(url, ffile, cookie_file):

    if cookie_file is not None:
        with open(cookie_file, "r") as f:
            cookie = f.read()
            f.close()
    else:
        cookie = None

    if ffile is not None:
        with open(ffile, "r") as f:
            lines = f.readlines()
            f.close()

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
            if cookie is not None:
                r_ = instaload2(l, cookie)
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
            return 0
        else:
            print("Unknown ERROR encountered: Downloads of one or more Posts may have failed!")
            return 1
    elif url is not None:
        if cookie is not None:
            r = instaload2(url, cookie)
            if r == 0:
                print("Download successfully!")
                return 0
            else:
                print("Unknown ERROR encountered: Download may have failed!")
                return 1
        else:
            r = instaload(url)
            if r == 0:
                print("Download successfully!")
                return 0
            else:
                print("Unknown ERROR encountered: Download may have failed!")
                return 1
    else:
        print("ERROR: You need to specify at least either -url, --url or -f, --file!")
        return 1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-url", "--url",
                        default = None,
                        dest = "url",
                        help = "The instagram URL to parse.",
                        type = str
                        )
    parser.add_argument("-f", "--file",
                        default = None,
                        dest = "file",
                        help = "A file containing instagram URLs to parse.",
                        type = str
                        )
    parser.add_argument("-c", "--cookie",
                        default = None,
                        dest = "cookie",
                        help = "A file containing cookie information for retrieving data.",
                        type = str
                        )
    args = parser.parse_args()

    print(download(args.url, args.file, args.cookie))

if __name__ == '__main__':
    main()
