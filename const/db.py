from tools.common import highlight
import requests
import json

db = json.loads(requests.get("https://ncov2019.oss-cn-beijing.aliyuncs.com/cache").text)["data"]

def date_contain(date, text):
    _, month, day = date.split("-")

    if f"{month}月{day}" in text:
        return True
    if f"{month}-{day}" in text:
        return True
    if month[0] == "0" and f"{month[1]}月{day}" in text:
        return True

    return False

def search(code, rel_text, reverse_check=False):
    result = []
    for i, element in enumerate(db):
        if not reverse_check:
            if code in element["t_no"]:
                s = f"\t [#{i + 1}]  {element['t_date']} | {highlight(element['t_no'], 32)} | {element['t_no_sub']} | 出发: {element['t_pos_start']} | 到达: {element['t_pos_end']}"
                result.append(s)
        else:
            if code in element["t_no"] and date_contain(element["t_date"], rel_text):
                s = f"\t [#{i + 1}]  {highlight(element['t_date'], 35)} | {highlight(element['t_no'], 32)} | {element['t_no_sub']} | 出发: {element['t_pos_start']} | 到达: {element['t_pos_end']}"
                result.append(s)
    return result