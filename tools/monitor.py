import crawler.weibo_crawler as weibo_crawler
import crawler.baidu_crawler as baidu_crawler
import const.db as db
import const.paths as paths
from const.raw import keyword_list
from tools.filter import find_codes
from tools.common import highlight, export_xlsx, empty_dir

import os
import json
import glob
import datetime

def is_added(idx):
    with open(paths.mark_filepath, "r") as f:
        data = json.load(f)
        return idx in data

def mark_added(idx):
    with open(paths.mark_filepath, "r") as f:
        data = json.load(f)
    if idx not in data:
        data.append(idx)
    with open(paths.mark_filepath, "w") as f:
        json.dump(data, f)

def is_star(idx):
    with open(paths.star_filepath, "r") as f:
        data = json.load(f)
        return idx in data

def mark_read_clue(t_clue):
    transfer_clue(t_clue, paths.unread_post_filepath, paths.read_post_filepath)

def star_clue(t_clue):
    idx = t_clue["id"]

    with open(paths.star_filepath, "r") as f:
        star_list = json.load(f)

    if idx in star_list:
        return

    star_list.append(idx)

    with open(paths.star_filepath, "w") as f2:
        json.dump(star_list, f2, indent=2)

    with open(paths.star_post_filepath, "r") as f2:
        data = json.load(f2)
        data.append(t_clue)

    with open(paths.star_post_filepath, "w") as f2:
        json.dump(data, f2, indent=2)

def unstar_clue(t_clue):
    idx = t_clue["id"]

    with open(paths.star_filepath, "r") as f:
        star_list = json.load(f)

    if idx not in star_list:
        return
    new_star_list = []
    for x in star_list:
        if x != idx:
            new_star_list.append(x)

    with open(paths.star_filepath, "w") as f:
        json.dump(new_star_list, f, indent=2)

    with open(paths.star_post_filepath, "r") as f:
        data = json.load(f)

    new_data = []

    for x in data:
        if x["id"] != idx:
            new_data.append(x)

    with open(paths.star_post_filepath, "w") as f:
        json.dump(new_data, f, indent=2)

def transfer_clue(t_clue, src, dst):

    with open(src, "r") as f:
        src_data = json.load(f)

    with open(dst, "r") as f:
        dst_data = json.load(f)

    remain_src = []

    for clue in src_data:
        if clue["id"] == t_clue["id"]:
            dst_data.append(clue)
        else:
            remain_src.append(clue)

    with open(paths.unread_post_filepath, "w") as f:
        json.dump(remain_src, f, indent=2)

    with open(paths.read_post_filepath, "w") as f:
        json.dump(dst_data, f, indent=2)

def add_clue_list(clue_list, filepath):

    with open(filepath, "r") as f:
        data = json.load(f)

    for clue in clue_list:
        if is_added(clue["id"]):
            continue
        data.append(clue)
        mark_added(clue["id"])

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

def add_clue(clue, filepath):

    if is_added(clue["id"]):
        return

    with open(filepath, "r") as f:
        data = json.load(f)

    data.append(clue)
    mark_added(clue["id"])

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

def process_posts(post_list):

    new_post_list = []

    for i, post in enumerate(post_list):

        print(f"\r\t正在处理第 {i + 1} 条，共 {len(post_list)} 条", end="", flush=True)
        text = post["text"]

        result = find_codes(text)

        for code, rel_text, rel_type in result:

            post["code"] = code
            post["rel_text"] = rel_text
            post["rel_type"] = rel_type
            new_post_list.append(post)

    add_clue_list(new_post_list, paths.unread_post_filepath)

def process_baidu():

    file_list = glob.glob(os.path.join(paths.baidu_path, "*.json"))

    for i, filename in enumerate(file_list):

        with open(filename, "r") as f:
            data = json.load(f)

        print(f"正在处理关于 {data['keyword']} 的搜索结果 ... [{i + 1}/{len(file_list)}]")

        post_list = []

        for post in data["data"]:
            post_list.append({
                "source" : "政府网站搜索",
                "id" : "bd_" + post["src_url"],
                "time" : "",
                "name" : "",
                "text" : post["text"],
                "src_url" : post["src_url"]
            })

        process_posts(post_list)

        print("")


def process_weibo():

    file_list = glob.glob(os.path.join(paths.weibo_path, "*.json"))

    for i, filename in enumerate(file_list):

        with open(filename, "r") as f:
            data = json.load(f)

        print(f"正在处理来自 {data['user']['screen_name']} 的微博 ... [{i + 1}/{len(file_list)}]")

        post_list = []

        for post in data["weibo"]:
            post_list.append({
                "source" : "微博",
                "id" : "wb_" + str(post["id"]),
                "time" : post["created_at"],
                "name" : post["screen_name"],
                "text" : post["text"],
                "src_url" : "https://m.weibo.cn/status/" + str(post["id"])
            })

        process_posts(post_list)

        print("")

def filter_posts(data):

    print(highlight(f"共 {len(data)} 条线索。"))

    author = input(highlight("指定来源微博 (不指定则为空，多个用空格隔开): "))

    author_list = author.split()

    start_date_str = input(highlight("输入开始日期 (yyyy-mm-dd): "))

    while True:
        try:
            if start_date_str != "":
                start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
            break
        except:
            print(highlight("请输入正确日期格式。"))

    end_date_str = input(highlight("输入结束日期 (yyyy-mm-dd): "))

    while True:
        try:
            if end_date_str != "":
                end_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
            break
        except:
            print(highlight("请输入正确日期格式。"))

    keyword_filter = input(highlight("输入 f 筛选不包含疫情关键字的线索: "))

    filter_type = input(highlight("输入 u 只显示未匹配线索，m 只显示匹配线索， a 显示所有线索（默认）: "))

    result = []

    for element in data:

        if len(author_list) > 0:
            ok = False
            for author in author_list:
                if author in element["name"]:
                    ok = True
            if not ok:
                continue

        try:
            clue_date = datetime.datetime.strptime(element["time"], "%Y-%m-%d")
        except:
            clue_date = None

        if keyword_filter == "f":

            contain_keyword = False

            for keyword in keyword_list:
                if keyword in element["rel_text"]:
                    contain_keyword = True
                    element["rel_text"] = element["rel_text"].replace(keyword, highlight(keyword, 35))

            if not contain_keyword:
                continue

        if clue_date and start_date_str != "" and clue_date < start_date:
            continue

        if clue_date and end_date_str != "" and clue_date > end_date:
            continue

        db_result, _ = db.search(element["code"], element["rel_text"], reverse_check=True)

        if filter_type == "u" and len(db_result) > 0:
            continue

        if filter_type == "m" and len(db_result) == 0:
            continue

        element["src_url"] = element["src_url"]

        result.append(element)

    return result

def print_stat(data):

    author_list = []
    author_count = {}

    date_list = []
    date_count = {}

    for element in data:

        author = element["name"]
        date = element["time"]

        if author not in author_list:
            author_list.append(author)
            author_count[author] = 0

        author_count[author] += 1

        if date not in date_list:
            date_list.append(date)
            date_count[date] = 0

        date_count[date] += 1

    print(highlight("\n来源统计: ", 33))

    sorted_author_list = sorted(author_count.items(), key=lambda item : item[1])
    for author, count in sorted_author_list:
        print(highlight(author, 31) + ": " + highlight(count, 32))

    print(highlight("\n日期统计: ", 33))

    sorted_date_list = sorted(date_count.items(), key=lambda item : item[1])
    for date, count in sorted_date_list:
        print(highlight(date, 31) + ": " + highlight(count, 32))

def display(filepath, catag):

    with open(filepath, "r") as f:
        data = json.load(f)

    filter_command = input(highlight("需要筛选吗 (y/n): "))

    if filter_command == "y":
        data = filter_posts(data)

    while True:

        command = input(f"\n载入 {len(data)} 条数据。输入 p - 导出到 xlsx，0 - 显示统计， 1 - 逐条显示，2 - 全部显示" +
                        ("，3 - 全部标记为已读" if catag == "unread" else "") +
                        "，q - 退出: ")

        if command == "p":
            export_xlsx(data)

        elif command == "0":
            print_stat(data)

        elif command == "1" or command == "2":

            for i, clue in enumerate(data):

                db_result, n_rel_text = db.search(clue["code"], clue["rel_text"], reverse_check=True)

                print(f"============================================================================")
                print(f"> [{i + 1}/{len(data)}]")
                print(highlight("是否标星", 33) + ("★" if is_star(clue["id"]) else ""))
                print(highlight("Post ID:", 33) + clue["id"])
                print(highlight("时间:", 33) + clue["time"])
                print(highlight("来源:", 33) + clue["source"] + " | " + clue["name"])
                print(highlight("网页:", 33) + clue["src_url"])
                print(highlight("相关编号:", 33) + clue["code"])
                print(highlight("上下文:", 33) + n_rel_text)
                print(highlight("类型:", 33) + clue["rel_type"])
                print(highlight("已存在数据: ", 33))
                for s in db_result:
                    print(s)
                print(f"============================================================================")

                if command == "1":
                    if catag == "unread":
                        print("输入 r 标记为已读，", end="")
                    next_step = input("(u)s （取消）标星该条数据，n 跳转到下一条，q 结束阅读。")
                    if next_step == "r" and catag == "unread":
                        mark_read_clue(clue)
                    elif next_step == "u":
                        unstar_clue(clue)
                    elif next_step == "s":
                        star_clue(clue)
                    elif next_step == "q":
                        break

        elif command == "3":
            if catag == "unread":
                for clue in data:
                    mark_read_clue(clue)
                print(f"已标记 {len(data)} 条数据为已读。")
            else:
                print("指令无效。")
        elif command == "q":
            break
        else:
            print("请输入正确的指令。")

def main():

    idx = input(highlight("请输入本次任务编号（用来避免重复爬取）:  "))

    paths.update_path(idx)

    while True:

        command = input(highlight("""\n1 - 爬取微博
2 - 对爬取微博进行索引（清空所有列表）
3 - 查看未处理相关新闻
4 - 查看已处理相关新闻
5 - 查看标星新闻
6 - 反向搜索航班/车次相关政府新闻
7 - 对政府新闻进行索引（清空所有列表）
8 - 清空下载内容
q - 退出: 

请输入指令: """, 31))

        if command == "1":
            weibo_crawler.main(save_path=paths.weibo_path)
        elif command == "2":
            paths.clear(idx)
            process_weibo()
        elif command == "3":
            display(paths.unread_post_filepath, "unread")
        elif command == "4":
            display(paths.read_post_filepath, "read")
        elif command == "5":
            display(paths.star_post_filepath, "star")
        elif command == "q":
            break
        elif command == "6":
            code_file = input(highlight("输入车次/航班列表 （留空则默认）:"))
            baidu_crawler.main(save_path=paths.baidu_path, file_path=code_file)
        elif command == "7":
            paths.clear(idx)
            process_baidu()
        elif command == "8":
            try:
                empty_dir(paths.baidu_path)
                empty_dir(paths.weibo_path)
                print(highlight("成功。"))
            except:
                print(highlight("失败。", 31))
        else:
            print("请重新输入指令。")

if __name__ == "__main__":
    main()