import requests
from tools import filter

if __name__ == "__main__":

    command = input("1 - 输入url，2 - 直接导入文本: ")

    if "1" in command:
        url = input("输入url: ")
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(url, headers=headers)
        r.encoding = "utf-8"
        filter.filter(r.text)
    else:
        path = input("输入文本文件: ")
        with open(path, "r") as f:
            text = f.read()
        filter.filter(text)