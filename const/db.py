from tools.common import highlight
import requests
import json

db = json.loads(requests.get("https://ncov2019.oss-cn-beijing.aliyuncs.com/cache").text)["data"]

def search(code):
    result = []
    for i, element in enumerate(db):
        if code in element["t_no"]:
            s = f"\t [#{i + 1}]  {element['t_date']} | {highlight(element['t_no'], 32)} \
            | {element['t_no_sub']} | 出发: {element['t_pos_start']} | 到达: {element['t_pos_end']}"
            result.append(s)
    return result