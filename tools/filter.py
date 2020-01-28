from const.code import flight_code, train_code, car_code
from const import db
from tools.common import highlight

L_PAD = 50
R_PAD = 50

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

def find_codes(text):

    result = []
    last = -1

    text = text + "#"

    for i, ch in enumerate(text):
        if is_alpha(ch) or ch.isdigit():
            if last == -1:
                last = i
        else:
            if last != -1:
                success, code, rel_text, rel_type = process(text, last, i)
                if success:
                    result.append((code, rel_text, rel_type))
                last = -1

    return result

def filter(text):

    def display(ls, single=False):

        for i, (code, rel_text, rel_type, db_result) in enumerate(ls):

            if single:
                print(rel_text)
            else:
                print(f"============================================================================")
                print(f"> [{i + 1}/{len(ls)}]")
                print(highlight("相关编号:", 33) + code)
                print(highlight("上下文:", 33) + rel_text)
                print(highlight("类型:", 33) + rel_type)
                print(highlight("已存在数据: ", 33))
                for s in db_result:
                    print(s)
                print(f"============================================================================")

    result = find_codes(text)

    unmatched = []
    matched = []

    unmatched_r = []
    matched_r = []

    for i, (code, rel_text, rel_type) in enumerate(result):

        db_result, db_result_r = db.search(code, rel_text), db.search(code, rel_text, True)

        if len(db_result) == 0:
            unmatched.append((code, rel_text, rel_type, db_result))
        else:
            matched.append((code, rel_text, rel_type, db_result))

        if len(db_result_r) == 0:
            unmatched_r.append((code, rel_text, rel_type, db_result_r))
        else:
            matched_r.append((code, rel_text, rel_type, db_result_r))

    while True:

        command = input(f"""
        \n检索完成。共检索条目{len(result)}条。
[c] - 只输出上下文，默认关闭, [r] - 反向检索日期，默认关闭 
输入u[c][r]查看未匹配条目，输入m[c][r]查看匹配条目，输入q退出: """)
        print("")

        if "q" in command:
            break
        elif "u" in command:
            if "r" in command:
                display(unmatched_r, "c" in command)
            else:
                display(unmatched, "c" in command)
        else:
            if "r" in command:
                display(matched_r, "c" in command)
            else:
                display(matched, "c" in command)
