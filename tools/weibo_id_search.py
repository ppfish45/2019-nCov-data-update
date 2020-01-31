# coding=gbk

from tools.common import highlight
from const.ua import random_ua

import requests
import re
import time
import random

from urllib import parse

if __name__ == '__main__':

    name_list = []

    final_name_list = []
    final_id_list = []

    print("请输入微博名，以#结束")

    while True:

        name = input()

        if name == "#":
            break

        name_list.append(name)

    for i, name in enumerate(name_list):

        print(f"{i} / {len(name_list)} ...")

        if name in final_name_list:
            continue

        for k in range(5):

            url = "https://s.weibo.com/user?q=" + parse.quote(name) + "&Refer=user_user"
            headers = {
                'User-Agent': random_ua()
            }
            r = requests.get(url, headers=headers)
            r.encoding = "utf-8"

            result = re.search(r"weibo.com/u/(\d+)", r.text)

            if result:
                final_name_list.append(name)
                final_id_list.append(result.group(1))
                print(highlight(name, 32) + " " + result.group(1))
                break
            else:
                print(highlight(name, 31))

            time.sleep(1)

        time.sleep(1 + random.randint(1, 2))

        if i % 15 == 0:
            time.sleep(7)

    print(f"name_list = {final_name_list}")
    print(f"id_list = {final_id_list}")
