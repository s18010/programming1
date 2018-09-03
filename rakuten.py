import requests, webbrowser, sys, re, json
from pprint import pprint
from bs4 import BeautifulSoup
from collections import OrderedDict

'''
グラムあたりの単価が低い順に表示(途中)
(.が入った重さを正規表現するとbase10 valueError)
'''

proxies = {"http": "172.16.40.1:8888", "https": "172.16.40.1:8888"}
url = requests.get("https://search.rakuten.co.jp/search/mall/%E3%83%9F%E3%83%83%E3%82%AF%E3%82%B9%E3%83%8A%E3%83%83%E3%83%84/", verify=False).content
soup = BeautifulSoup(url)

api = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?applicationId=1098885711835405419&keyword=ミックスナッツ"
res = requests.get(api)
json_data = json.loads(res.text)

result = json_data["Items"]


def item_name(n):
    '''
    商品名を取得
    (itemNameの個数がわからないので、一旦適当な数を取得)
    '''
    name_list = []
    for i in range(n):
        name_list.append((result[i]["Item"]["itemName"]))
    return(name_list)


def item_url(n):
    '''
    URLを取得
    '''
    url_list = []
    for i in range(n):
        url_list.append((result[i]["Item"]["itemUrl"]))
    return(url_list)


def item_price(n):
    '''
    商品の価格を取得
    '''
    price_list = []
    for i in range(n):
        price_list.append((result[i]["Item"]["itemPrice"]))
    return price_list


def weight(n):
    '''
    各商品の名前から重さのみを取得(kgはgに変換)
    '''
    weight_list = []
    pattern = re.compile(r"(\d+)(kg|g)")

    for word in item_name(n):
        i = pattern.search(word)
        if i is None:
            weight_list.append(1)
        elif i.group(2) == "kg":
            weight_list.append(int(i.group(1)) * 1000)
        else:
            weight_list.append(int(i.group(1)))
    return weight_list


# 商品の単価を計算
yen_per_kg = [x / y for (x, y) in zip(item_price(30), weight(30))]


# 商品名を安い順に並べる
price_dict = sorted(dict(zip(yen_per_kg, item_name(30))).items())
sorted_title_list = [i[1] for i in price_dict]


# URLを安い順に並べる
url_dict = sorted(dict(zip(yen_per_kg, item_url(30))).items())
sorted_url_list = [i[1] for i in url_dict]


def item_url():
    '''
    itemとurlをくっつける
    '''
    item_url = list(zip(sorted_title_list, sorted_url_list))
    return item_url


print("\単価が安い順ランキング/")
for i, name in enumerate(item_url(), 1):
    print("{}位: ".format(i), name[0])
    print(name[1])
    print()
