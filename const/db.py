from tools.common import highlight
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

def search(code, rel_text, reverse_check=False):

    result = []
    dates = []

    for i, element in enumerate(db):

        if code.replace(" ", "") == element["t_no"].replace(" ", ""):
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

    new_rel_text = rel_text

    for x in dates:
        new_rel_text = new_rel_text.replace(x, highlight(x, 35))

    return result, new_rel_text