from const.raw import raw_ua_list
import random

ua_list = []

for element in raw_ua_list:
    if "Windows" in element["ua"] or "Mac" in element["ua"]:
        ua_list.append(element["ua"])

def random_ua():
    idx = random.randint(0, len(ua_list) - 1)
    return ua_list[idx]