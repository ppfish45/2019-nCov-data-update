from tools.common import highlight, find_codes, find_plain_code
import requests
import json

try:
    db = json.loads(requests.get("http://2019ncov2.toolmao.com/ncovadmin/list").text)["data"]
    print(highlight(f"导入已录入信息 {len(db)} 条。"))
except:
    try:
        db = json.loads(requests.get("http://2019ncov.nosugartech.com/data.json").text)["data"]
        print(highlight(f"导入已录入信息 {len(db)} 条。"))
    except:
        print(highlight(f"导入已录入信息失败。"))

def date_contain(date, text):
    _, month, day = date.split("-")

    months = [month]
    days = [day]

    if month[0] == "0":
        months.append(month[1])

    if day[0] == "0":
        days.append(day[1])

    for m in months:
        for d in days:
            if f"{m}月{d}日" in text:
                return True, f"{m}月{d}日"
            if f"{m}月{d}" in text:
                return True, f"{m}月{d}"
            if f"{m}.{d}" in text:
                return True, f"{m}.{d}"
            if f"{m}-{d}" in text:
                return True, f"{m}-{d}"
            if f"{m}-{d}" in text:
                return True, f"{m}/{d}"
    for d in days:
        if f"{d}日" in text:
            return True, f"{d}日"

    return False, ""

def db_unique(f_type):

    def match(text1, text2):

        text1 = text1.upper()
        text2 = text2.upper()

        code_in_txt1 = [x for x in find_plain_code(text1)]
        code_in_txt2 = [x for x in find_plain_code(text2)]

        for code in code_in_txt1:
            if code in code_in_txt2:
                return True

        return False

    for i in range(len(db)):

        for j in range(i + 1, len(db)):

            data1 = db[i]
            data2 = db[j]

            if data1["t_type"] != f_type or data2["t_type"] != f_type:
                continue

            if match(data1["t_no"], data2["t_no"]) and data1["t_date"] == data2["t_date"]:

                if data1["t_type"] == 2 and data2["t_type"] == 2 and not match(data1["t_no_sub"], data2["t_no_sub"]):
                    continue

                if data1["verified"] != 2 and data2["verified"] != 2:

                    print("=" * 100)
                    print(highlight(f"id = {data1['id']} :"))
                    print(data1)
                    print(highlight(f"id = {data2['id']} :"))
                    print(data2)
                    print("=" * 100)

def search(code, rel_text, reverse_check=False):

    result = []
    dates = []

    code = code.upper().replace(" ", "")

    for i, element in enumerate(db):

        code_in_no = find_codes(element["t_no"].replace(" ", ""))

        for t_no, _ , _ in code_in_no:

            if code == t_no:
                date_ok, date_key = date_contain(element["t_date"], rel_text)

                if element["verified"] == 1:
                    verified = highlight("已审核")
                elif element["verified"] == 0:
                    verified = highlight("未处理", 31)
                else:
                    verified = highlight("未通过", 31)

                if date_ok:
                    s = f"\t [#{i + 1}]  {highlight(element['t_date'], 35)} | {highlight(element['t_no'], 32)} | {element['t_no_sub']} | 出发: {element['t_pos_start']} | 到达: {element['t_pos_end']} | {verified}"
                    dates.append(date_key)
                else:
                    s = f"\t [#{i + 1}]  {element['t_date']} | {highlight(element['t_no'], 32)} | {element['t_no_sub']} | 出发: {element['t_pos_start']} | 到达: {element['t_pos_end']} | {verified}"

                if date_ok or not reverse_check:
                    result.append(s)

                break

    new_rel_text = rel_text

    for x in dates:
        new_rel_text = new_rel_text.replace(x, highlight(x, 35))

    return result, new_rel_text

if __name__ == "__main__":
    filter_type = int(input(highlight("请输入筛选类型: ")))
    db_unique(f_type=filter_type)