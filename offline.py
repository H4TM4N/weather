import sys
try:
	import csv
	import prettytable
except ImportError:
	print("[Error] can't import modules")
	sys.exit()

try:
	fp = open("data.csv","r")
	table = prettytable.from_csv(fp)
	print(table)
	fp.close()
except FileNotFoundError:
	print("[Error] Data not found")

