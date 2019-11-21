#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# ########
# 気象庁(http://www.jma.go.jp/)から天気予報を取得するプログラム
# 地域指定はコマンドライン引数に何か追加する(引数が1以上なら地域選択)
# 引数がなければ前回選択した地域の天気予報を表示する
# かなり強引なコーディングである為,対象html仕様が変われば動作しないと思われる
# 最終テスト日: 2019/01/23
#   OS: Ubuntu16.04 LTS
# ########

import sys

try:
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    import os
except ImportError:
    print("[Error] {0}".format(sys.exc_info()[1]))
    print('[Info ] Please type command "$ pip3 install BeautifulSoup4"')
    sys.exit()
TODAY = 0
TOMORROW = 1

days = [TODAY, TOMORROW]

LOGFILE = ".forecast_log"


# 地域選択
def select_area():
    url = "http://www.jma.go.jp/jp/yoho/"
    html = urlopen(url)
    bs = BeautifulSoup(html, "html.parser")
    area_div = bs.select("div#area > table > tr")[0]
    area_table = area_div.select("td")[3]
    areas = area_table.select("option")[1:]
    idx = 1
    print("番号を選んでください")
    for area in areas:
        print("\t{0}\t{1}".format(idx, area.getText()))
        idx += 1
    print(">>")
    num = int(input())
    if not num in range(1, idx):
        print("[Error] Invalid input")
        return select_area()
    url += str(num + 300) + ".html"
    print(url)
    with open(LOGFILE, "a") as f:
        f.write(url)
    # setSearchQuery(url)
    # print(url)
    return url


# 地方選択
def select_region(table):
    regions = table.select("th.th-area")
    idx = 0
    print("地方を選んでください")
    for region in regions:
        print("\t{0}\t{1}".format(idx, region.find("div").get_text()))
        idx += 1
    print(">>")
    num = int(input())
    if not num in range(0, idx):
        print("[Error] Invalid input")
        return select_region(table)
    with open(LOGFILE, "a") as f:
        f.write("\t" + str(num) + "\n")
    return num


# 日付と天気
def get_date_weather(day, table):
    cols = table.select("tr > th.weather")
    date = cols[day].get_text().replace("\n", "")
    weather = cols[day].find("img", alt=True)["alt"]
    return "{0} {1}\n".format(date, weather)


# 降水確率
def get_rain(day, table):
    raind = table.select("tr > td.rain")
    rain_table = raind[day].find("table")
    rain_tds = rain_table.select("td")
    time = []
    per = []
    idx = 0
    for td in rain_tds:
        if idx % 2 == 0:
            time.append(td.get_text() + "時")
        else:
            per.append(td.get_text())
        idx += 1
    time_str = "\t".join(time)
    per_str = "\t".join(per)
    return "降水確率:\n{0}\n{1}\n".format(time_str, per_str)


# 気温
def get_temp(day, table):
    temp = table.select("tr > td.temp")
    temp_colm = temp[day].select("tr > td")
    if len(temp_colm) == 0:
        return ""
    min_temp = "最低気温: " + temp_colm[1].get_text()
    max_temp = "最高気温: " + temp_colm[2].get_text()
    if not temp_colm[1].get_text() and temp_colm[2].get_text():
        return "{0}\n".format(max_temp)
    else:  # 最低気温が空でない場合
        return "{0}\n{1}\n".format(min_temp, max_temp)


# 過去ログ検索
def get_log():
    try:
        with open(os.path.dirname(__file__).replace(".", "") + LOGFILE, "r") as f:
            liner = f.readlines()
            if len(liner) > 0:
                return liner[len(liner) - 1].replace("\n", "")
            else:
                print("[Error] DATA NOT EXIST")
                # Default Data(鳥取県 東部)
                return "http://www.jma.go.jp/jp/yoho/339.html\t0"
    except FileNotFoundError:
        print("[Error] No such File {0}".format(os.path.dirname(__file__) + LOGFILE))
        print("[Error] Please type $ ./forecast.py -a")
        # print("[Info ] Now execute on {0}".format(os.getcwd()))
        # print("[Info ] executing file is {0}".format(__file__))
        # print("[Info ] Folder name is {0}".format(os.path.dirname(__file__)))
        sys.exit()


# main method
if __name__ == "__main__":
    args = sys.argv
    # Default Data(鳥取県 東部)
    url = "http://www.jma.go.jp/jp/yoho/339.html"
    region = 0
    if len(args) > 1:
        url = select_area()
        bs = BeautifulSoup(urlopen(url), "html.parser")
        main_table = bs.select("table.forecast")[0]
        region = select_region(main_table)
    else:
        log = get_log().split("\t")
        url = log[0]
        region = log[1]
        bs = BeautifulSoup(urlopen(log[0]), "html.parser")
        main_table = bs.select("table.forecast")[0]

    place = bs.find("h1").get_text().replace("\n", "")
    area = main_table.select("th.th-area")[int(region)].find("div").get_text()
    print(place, area)
    print("-----------------")
    for day in days:
        print(get_date_weather(day, main_table))
        print(get_rain(day, main_table))
        print(get_temp(day, main_table))
    print("Sourced from {0}".format(url))
