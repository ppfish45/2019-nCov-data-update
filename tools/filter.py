from const import db
from const.raw import keyword_list
from tools.common import highlight, export_xlsx
from crawler.browser import browser
from tools.ocr import ocr_text

import pandas as pd
from tools.common import find_codes

def display(ls, single=False):

    for i, (code, rel_text, rel_type, db_result) in enumerate(ls):

        if single:
            print(f"============================================================================")
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

def filter_xlsx(xlsx_path):

    df = pd.read_excel(xlsx_path, header = [0])

    matched = []
    unmatched = []

    df_remain = pd.DataFrame(columns=df.columns)

    for i in range(df.shape[0]):

        row = df.loc[i].values
        raw_str = ""

        for item in row:
            raw_str = raw_str + " | " + str(item)

        result = find_codes(raw_str)
        ok = False

        for code, rel_text, rel_type in result:

            db_result, n_rel_text = db.search(code, rel_text, reverse_check=True)

            if len(db_result) == 0:
                unmatched.append((code, n_rel_text, rel_type, db_result))
            else:
                matched.append((code, n_rel_text, rel_type, db_result))
                ok = True

        if not ok:
            df_remain.loc[df_remain.shape[0]] = df.loc[i]

    while True:

        command = input(highlight(f"""
        \n检索完成。共检索条目{len(matched) + len(unmatched)}条。 
输入 u[c] 查看未匹配条目，输入 m[c] 查看匹配条目，输入 q 退出，输入 s 保存未匹配: """, 31))
        print("")

        if "q" in command:
            break
        elif "u" in command:
            display(unmatched, "c" in command)
        elif "m" in command:
            display(matched, "c" in command)
        elif "s" in command:
            filepath = input(highlight("请输入保存文件名 (xlsx): "))
            writer = pd.ExcelWriter(filepath)
            df_remain.to_excel(writer, header=True)
            writer.save()

def filter(text):

    need_keyword = input(highlight("是否需要检索关键词? (y/n): "))

    print(highlight("开始检索..."))

    result = find_codes(text)

    unmatched = []
    matched = []

    unmatched_r = []
    matched_r = []

    export_data = []

    for i, (code, rel_text, rel_type) in enumerate(result):

        if need_keyword == "y":
            ok = False
            for keyword in keyword_list:
                if keyword in rel_text:
                    ok = True
            if not ok:
                continue

        db_result, n_rel_text = db.search(code, rel_text)

        if len(db_result) == 0:
            unmatched.append((code, n_rel_text, rel_type, db_result))
        else:
            matched.append((code, n_rel_text, rel_type, db_result))

        db_result_r, n_rel_text_r = db.search(code, rel_text, True)

        if len(db_result_r) == 0:
            unmatched_r.append((code, n_rel_text_r, rel_type, db_result_r))
            export_data.append({
                "code" : code,
                "rel_text" : rel_text
            })
        else:
            matched_r.append((code, n_rel_text_r, rel_type, db_result_r))

    while True:

        command = input(highlight(f"""
        \n检索完成。共检索条目{len(result)}条。
[c] - 只输出上下文，默认关闭, [r] - 反向检索日期，默认关闭 
输入u[c][r]查看未匹配条目，输入m[c][r]查看匹配条目，
输入 s 将保存未匹配条目
输入q退出: """, 31))

        print("")

        if "q" in command:
            break
        elif "u" in command:
            if "r" in command:
                display(unmatched_r, "c" in command)
            else:
                display(unmatched, "c" in command)
        elif "m" in command:
            if "r" in command:
                display(matched_r, "c" in command)
            else:
                display(matched, "c" in command)
        elif "s" in command:
            export_xlsx(export_data, columns=["相关文本", "相关编号"], ids=["rel_text", "code"])

def filter_urls(data):

    need_keyword = input(highlight("是否需要检索关键词? (y/n): "))

    print(highlight("开始检索..."))

    unmatched = []
    matched = []
    export_data = []

    for item in data:

        text = item["text"]
        url = item["url"]

        if url == "":
            continue

        result = find_codes(text)

        for i, (code, rel_text, rel_type) in enumerate(result):

            if need_keyword == "y":
                ok = False
                for keyword in keyword_list:
                    if keyword in rel_text:
                        ok = True
                if not ok:
                    continue

            db_result, n_rel_text = db.search(code, rel_text, reverse_check=True)

            if len(db_result) == 0:
                unmatched.append((code, n_rel_text, rel_type, db_result))
                export_data.append({
                    "code" : code,
                    "rel_text" : rel_text,
                    "src_url" : url
                })
            else:
                matched.append((code, n_rel_text, rel_type, db_result))

    while True:

        command = input(highlight(f"""
        \n检索完成。共检索条目{len(matched) + len(unmatched)}条。
[c] - 只输出上下文，默认关闭。
输入 u[c] 查看未匹配条目，
输入 m[c] 查看匹配条目，
输入 s 将保存未匹配条目
输入q退出: """, 31))
        print("")

        if "q" in command:
            break
        elif "u" in command:
            display(unmatched, "c" in command)
        elif "m" in command:
            display(matched, "c" in command)
        elif "s" in command:
            export_xlsx(export_data, columns=["相关文本", "相关编号", "来源网址"], ids=["rel_text", "code", "src_url"])

def main():

    while True:

        command = input(highlight("""\n1 - 输入url
2 - 直接导入文本
3 - 导入xlsx
4 - 导入图片
q - 退出:

请输入指令: """, 31))

        if command == "1":
            print(highlight("输入url, 以#结束: "))

            url_data = []

            crawler = browser()

            while True:
                url = input()

                if url == "":
                    continue
                if url == "#":
                    break

                url_data.append({
                    "url" : url,
                    "text" : crawler.get_result(url, plain=True)
                })

            filter_urls(url_data)
        elif command == "2":
            path = input("输入文本文件: ")
            with open(path, "r") as f:
                text = f.read()
            filter(text)
        elif command == "3":
            path = input("输入 xlsx 文件: ")
            filter_xlsx(path)
        elif command == "4":
            path = input("输入图片文件: ")
            text = ocr_text(path)
            filter(text)
        elif command == "q":
            break
        else:
            print("请输入正确指令。")

if __name__ == "__main__":
    main()
