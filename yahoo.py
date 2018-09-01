#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests
import tkinter.messagebox as mb

url = requests.get("https://stocks.finance.yahoo.co.jp/stocks/detail/?code=GBPJPY=X").content
soup = BeautifulSoup(url, "html.parser")
price = soup.select_one(".stoksPrice").text

ans = mb.askokcancel("Yahoo Finance", "現在の英ポンド/円の為替相場を確認しますか？")
if ans:
    mb.showinfo("Yahoo Finance", "GBP/JPY={}".format(price))
else:
    mb.showinfo("Yahoo Finance", "OKボタンを押して終了")
