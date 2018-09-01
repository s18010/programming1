#!/usr/bin/python3
import os, requests
from bs4 import BeautifulSoup

'''
ブログ内の写真をまとめてダウンロードする
'''
url = requests.get("https://www.zoella.co.uk/2016/09/my-happy-place-autumn-touches.html")
os.makedirs("zoe_images", exist_ok=True)
soup = BeautifulSoup(url.text)

images = soup.select("#post-5481 img[src]")
for i in range(len(images)):
    if images == []:
        print("no image is found")
    else:
        images_url = images[i].get("src")
        print("downloading")
        res = requests.get(images_url)

    image_file = open(os.path.join("zoe_images", os.path.basename(images_url)), "wb")
    for chunk in res.iter_content(10000):
        image_file.write(chunk)
    image_file.close()
