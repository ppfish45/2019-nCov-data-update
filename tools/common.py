import const.paths as paths
from const.code import flight_code, train_code, car_code, all_train

import os
import glob
import json
import requests
import pandas as pd

L_PAD = 150
R_PAD = 150

def get_real_url(url, timeout=10):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=headers, timeout=timeout)
    return r.url

def highlight(text, color=32, space=True):
    if space:
        return f"\033[1;{color};20m {text} \033[0m"
    else:
        return f"\033[1;{color};20m{text}\033[0m"

def is_scanned(name):

    with open(paths.account_filepath, "r") as f:
        data = json.load(f)
        if name in data:
            return True

    return False

def add_scanned(name):

    with open(paths.account_filepath, "r") as f:
        data = json.load(f)
    with open(paths.account_filepath, "w") as f:
        data.append(name)
        json.dump(data, f)

def relative_text(text, l, r):
    left = text[0 : l].split("\n")[-1]
    right = text[r : len(text)].split("\n")[0]
    left = left[-L_PAD:]
    right = right[:R_PAD]
    return left + highlight(text[l : r]) + right

def is_alpha(text):
    order = ord(text)
    if ord("a") <= order <= ord("z"):
        return True
    if ord("A") <= order <= ord("Z"):
        return True
    return False

def contain_digit(text):
    for ch in text:
        if ch.isdigit():
            return True
    return False

def contain_alpha(text):
    for ch in text:
        if is_alpha(ch):
            return True
    return False

def is_flight(text):
    return contain_digit(text) and text[:2] in flight_code and not contain_alpha(text[2:]) and 5 <= len(text) <= 6

def is_train(text):
    if text in all_train:
        return True
    return contain_digit(text) and text[:1] in train_code and not contain_alpha(text[1:]) and 2 <= len(text) <= 6

def is_car(text):
    return contain_digit(text) and text[:2] in car_code and 2 <= len(text) <= 9

def process(text, l, r):

    code = text[l : r]

    if is_train(code):
        return True, text[l : r], relative_text(text, l, r), "TRAIN"

    if is_car(text[l - 1 : r]):
        return True, text[l - 1 : r], relative_text(text, l - 1, r), "CAR"

    if is_flight(code):
        return True, text[l : r], relative_text(text, l, r), "FLIGHT"

    if text[r] == "路":
        return True, text[l : r + 1], relative_text(text, l, r + 1), "BUS"

    if text[r : r + 2] == "号线":
        return True, text[l : r + 2], relative_text(text, l, r + 2), "SUBWAY"

    return False, "", "", ""

def find_plain_code(text):
    result = []
    last = -1

    text = text + "#"

    for i, ch in enumerate(text):
        if is_alpha(ch) or ch.isdigit() or ch == "-":
            if last == -1:
                last = i
        else:
            if last != -1:
                result.append(text[last:i].upper())
                last = -1

    return result

def find_codes(text):

    result = []
    last = -1

    text = text + "#"

    for i, ch in enumerate(text):
        if is_alpha(ch) or ch.isdigit() or ch == "-":
            if last == -1:
                last = i
        else:
            if last != -1:
                success, code, rel_text, rel_type = process(text, last, i)
                code = code.upper()
                if success:
                    result.append((code, rel_text, rel_type))
                last = -1

    return result

def export_xlsx(data,
                columns=["发布时间", "相关文字", "相关编号", "来源网址", "来源", "发布人"],
                ids=["time", "rel_text", "code", "src_url", "source", "name"]):

    filename = input(highlight("保存到文件名 (xlsx): "))

    writer = pd.ExcelWriter(filename)

    count = len(data)

    df_data = dict()

    for i, col in enumerate(columns):
        df_data[col] = [de_highlight(item[ids[i]]) for item in data]

    df = pd.DataFrame(df_data, columns=columns, index=[str(x + 1) for x in range(count)])

    try:
        df.to_excel(writer, header=True, index=True)
        writer.save()
        print(highlight("写入成功。"))
    except:
        print(highlight("写入失败。"))

def de_highlight(s):

    for color_id in range(0, 40):
        s = s.replace(f"\033[1;{color_id};20m", "")
        s = s.replace(f"\033[0m", "")

    return s

def empty_dir(dir):
    for filename in glob.glob(os.path.join(dir, "*.*")):
        os.remove(filename)