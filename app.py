from tools import filter, monitor
from tools.common import highlight

if __name__ == "__main__":

    while True:

        command = input(highlight("""\n1 - 手动检索新闻 / 文本文件 / xlsx 表格 / 图片
2 - 新闻实时跟踪
q - 退出:

请输入指令: """, 31))

        if command == "1":
            filter.main()
        elif command == "2":
            monitor.main()
        elif command == "q":
            break
        else:
            print("请输入正确的指令。")