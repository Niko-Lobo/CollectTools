import datetime
import time
import xlrd


config = {}


def read_config():
    rd = xlrd.open_workbook('Configure.xlsx')
    sheet = rd.sheet_by_index(0)
    for rownumb in range(1,sheet.nrows):
        row = sheet.row_values(rownumb)
        config[row[0]] = row[1]

read_config()
print (config['max_time_out'])
print(datetime.datetime.today().isoweekday())
a = time.asctime().split(' ')
print(int((a[3].split(':'))[0] )+int((a[3].split(':'))[1]) )
# if a[3]>16:
#     print(true)