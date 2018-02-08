import sys
try:
	import csv
	from urllib.request import urlopen
	from bs4 import BeautifulSoup
	import prettytable

except ImportError:
	print("[Error] can't import modules")
	sys.exit()

html = urlopen("http://www.jma.go.jp/jp/amedas_h/today-69122.html?areaCode=000&groupCode=52")
bs = BeautifulSoup(html,"html.parser")

table = bs.find("table",id="tbl_list")
rows = table.findAll("tr")
place = bs.find("td",class_="td_title height2")
placeSub = bs.find("td",class_="td_subtitle height1")
csvFile = open("data.csv","wt",newline = '',encoding = 'utf-8')
writer = csv.writer(csvFile)
time = bs.findAll("div")[25]

try:
	for row in rows:
		csvRow = []
		for cell in row.findAll(['td']):
			csvRow.append(cell.get_text())
		writer.writerow(csvRow)

finally:
	csvFile.close()

fp = open("data.csv","r")
showTable = prettytable.from_csv(fp)
fp.close()
print(place.get_text())
print(time.get_text())
print(showTable)


