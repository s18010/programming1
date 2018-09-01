#!/usr/bin/python3

import requests, bs4, webbrowser

'''
ブログ内のSNSサイトをまとめて開く
'''
proxies = {"http": "172.16.40.1:8888", "https": "172.16.40.1:8888"}
url = requests.get("https://www.zoella.co.uk/", proxies=proxies, verify=False)

soup = bs4.BeautifulSoup(url.text)
elems = soup.select("a")

list = []
href = 0
for i in elems:
    if href > 5:
        break
    else:
        list.append(i.get("href"))
        href += 1
for n in range(len(list)):
    webbrowser.open(list[n])
