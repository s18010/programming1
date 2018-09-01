import requests, webbrowser, sys, re, json
from pprint import pprint
from bs4 import BeautifulSoup

'''
gあたりの単価が低い順に表示(途中)
'''

proxies = {"http": "172.16.40.1:8888", "https": "172.16.40.1:8888"}
url = requests.get("https://search.rakuten.co.jp/search/mall/%E3%83%9F%E3%83%83%E3%82%AF%E3%82%B9%E3%83%8A%E3%83%83%E3%83%84/", verify=False).content
soup = BeautifulSoup(url)


def title():
    '''
    商品名を取得
    '''
    title_list = []
    for item in soup.find_all("a", attrs={"data-track-trigger": "title", "target": "_top"}):
        title = item.get("title")
        if title is None:
            continue
        title_list.append(title)
    return title_list


def weight():
    '''
    各商品の重さのみを取得(kgはgに変換)
    '''
    weight_list = []
    pattern = re.compile(r"(\d+)(kg|g)")

    for word in title():
        i = pattern.search(word)
        if i is None:
            weight_list.append(1)
        elif i.group(2) == "kg":
            weight_list.append(int(i.group(1)) * 1000)
        else:
            weight_list.append(int(i.group(1)))
    return weight_list


def price():
    '''
    商品の価格を取得
    '''
    price_list = []
    for item in soup.select(".important"):
        price_list.append(item.text)
    return price_list


def price_num():
    '''
    価格の数字のみ取得
    '''
    plist = []
    pattern = re.compile(r"(\d,\d+)円")
    for word in price():
        i = pattern.search(word)
        if i is None:
            plist.append(1)
        else:
            plist.append(int(i.group(1).replace(",", "")))
    return plist


def take_source():
    '''
    URLを取得
    '''
    api = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?applicationId=1098885711835405419&keyword=ミックスナッツ"
    res = requests.get(api)
    json_data = json.loads(res.text)
    result = json_data["Items"]
    pprint(json_data)

    url_list = []
    for i in range(30):
        url_list.append((result[i]["Item"]["itemUrl"]))
    print(url_list)


take_source()


'''
商品の単価を計算
yen_per_kg = [x / y for (x, y) in zip(price_num(), weight())]
print(yen_per_kg)
'''
