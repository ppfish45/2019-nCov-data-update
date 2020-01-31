from const.raw import keyword_list
from tools.common import highlight

from crawler import browser
from bs4 import BeautifulSoup

import os
import json
import glob

class baidu_crawler:

    def __init__(self):
        self.browser = browser.browser()
        pass

    def get_result(self, keyword, pages=1):
        result = []

        for page in range(pages):

            url = "https://www.baidu.com/s?wd=" + keyword + "&pn=" + str(page) + "0"
            text = self.browser.get_result(url)

            soup = BeautifulSoup(text, "html.parser")
            result_divs = soup.find_all("div", {"class" : "c-abstract"})
            result_urls = soup.find_all("a", {"class" : "c-showurl"})

            for i in range(len(result_divs)):
                result.append({
                    "text" : result_divs[i].get_text(),
                    "src_url" : result_urls[i]["href"]
                })

        return result

def main(save_path, file_path=""):

    if file_path == "":
        code_list = keyword_list
    else:
        with open(file_path, "r") as f:
            code_list = f.readlines()

    page_num = int(input(highlight("请输入搜索页数: ")))

    crawler = baidu_crawler()

    exist_list = []

    for filename in glob.glob(os.path.join(save_path, "*.json")):
        name = os.path.split(filename)[-1].split(".")[0]
        exist_list.append(name)

    for i, code in enumerate(code_list):
        print(highlight(f"[{i + 1} / {len(code_list)}] 正在搜索 {code} ..."))
        if code in exist_list:
            print(highlight("跳过，因为已经搜索过。"))
        result = crawler.get_result(code + " site:gov.cn", pages=page_num)
        with open(os.path.join(save_path, code + ".json"), "w") as f:
            json.dump({
                "keyword" : code,
                "data": result
            }, f)

if __name__ == "__main__":
    main(".")