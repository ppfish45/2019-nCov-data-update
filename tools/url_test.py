from const.db import db
from tools.common import highlight
from tools.common import find_codes

from difflib import SequenceMatcher
import requests

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def main():

    fail_list = []

    for i, item in enumerate(db):

        print(f"{i + 1} / {len(db)} ... ", end="", flush=True)

        url = item["source"]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(url, headers=headers)
        r.encoding = "utf-8"

        result = find_codes(item["t_no"])
        if len(result) > 0:
            idx, _, _ = result[0]
        else:
            idx = item["t_no"]
        codes = find_codes(r.text)

        print("\r", end="")

        ok = False

        for code, _, _ in codes:
            if similarity(code, idx) > 0.3:
                ok = True
                break

        if ok:
            continue

        if idx in r.text:
            continue

        print(highlight(f"NO id = {item['id']} | ", 31) + " " + item["source"] + " " + item["t_no"])
        fail_list.append(item["id"])

if __name__ == "__main__":
    main()