from crawler.browser import browser
from bs4 import BeautifulSoup
from tools.common import highlight

equiv_station = {
    "武汉" : ["武昌", "汉口"]
}

def equiv(probe, target):
    if probe in target or target in probe:
        return True, probe
    if target in equiv_station:
        for station in equiv_station[target]:
            if probe == station:
                return True, station
    return False, target

class Searcher():

    def __init__(self):
        self.browser = browser()

    def search_time(self, code, start_station, end_station):

        url = "https://qq.ip138.com/train/" + code + ".htm"
        text = self.browser.get_result(url)
        soup = BeautifulSoup(text, "html.parser")
        trs = soup.find_all("tr", {"onmouseover" : "this.bgColor='#E6F2E7';"})

        result = dict()

        for tr_text in trs:
            tds = tr_text.find_all("td")
            result[tds[1].get_text()] = tds[3].get_text()

        start_time = ""
        end_time = ""
        new_start = ""
        new_end = ""

        for station in result:
            ret, new_start = equiv(station, start_station)
            if ret:
                start_time = result[station]
            ret, new_end = equiv(station, end_station)
            if ret:
                end_time = result[station]

        return start_time, end_time, new_start, new_end

if __name__ == "__main__":

    print(highlight("请输入火车信息: 日期 - 车次 - 出发站 - 结束站，以#结束:"))
    infos = []

    while True:
        text = input()
        if text == "#":
            break
        info = text.split()
        infos.append({
            "date" : info[0],
            "code" : info[1],
            "start" : info[2],
            "end" : info[3]
        })

    searcher = Searcher()

    for info in infos:
        t_start, t_end, info["start"], info["end"] = searcher.search_time(info["code"], info["start"], info["end"])

        if t_start == "" or t_end == "":
            print(highlight(
                f"{info['date']}, {info['code']}, {info['date']+ ' ' + t_start}, {info['date'] + ' ' + t_end}, {info['start']}, {info['end']}", 31, space=False))
        else:
            print(f"{info['date']}, {info['code']}, {info['date']+ ' ' + t_start}, {info['date'] + ' ' + t_end}, {info['start']}, {info['end']}")
