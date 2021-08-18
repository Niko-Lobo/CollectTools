import csv
import xlrd
import easygui
import re
import datetime
import time
import json
import requests


def find_numb_cell(arg1_data_row, arg2_find):
    numb_cell = 0
    while numb_cell != 4:
        if arg2_find in arg1_data_row[numb_cell]:
            # print('find ' + str(arg2_find) + ' in ' + str(numb_cell) + ' cell')
            break
        else:
            numb_cell += 1
    if numb_cell == 4:
        pass
    else:
        return numb_cell


def detect_all_cell_numb(arg1_row, arg2_name_database, arg3_sheet=None, arg4_rd=None, arg5_rownumber=None):
    if find_numb_cell(arg1_row, '@'):
        temp = [0, 1, 2, 3]
        mail = find_numb_cell(arg1_row, '@')
        data = '000'
        name = '000'
        transaction = '000'
        temp.remove(mail)
        for i in temp:
            try:
                if re.findall('\d{4}-\d{2}-\d{2}|\d{2}.\d{2}.\d{4}|\d{2}.\d{2}.\d{2}', str(arg1_row[i])):
                    data = i
                    temp.remove(data)
                elif arg3_sheet != None:
                    if arg3_sheet.cell(arg5_rownumber, i).ctype == 3:  # xldate
                        year, month, day, hour, minute, second = xlrd.xldate_as_tuple((arg1_row[i]), arg4_rd.datemode)
                        data = i
                        temp.remove(data)
            except IndexError:
                pass
        for i in temp:
            if arg1_row[i].lower().strip() in arg2_name_database:
                name = i
                temp.remove(name)
        if len(temp) == 1:
            transaction = temp[0]
        dict_numb_cell['mail'] = mail
        dict_numb_cell['data'] = data
        dict_numb_cell['name'] = name
        dict_numb_cell['transaction'] = transaction
        return dict_numb_cell


def read_and_send_file_csv(arg1_file_name, arg2_name_database):
    with open(arg1_file_name, 'r', encoding='cp1251', newline='') as f:
        reader = csv.reader(f, delimiter=';')
        for r in reader:
            if detect_all_cell_numb(r, arg2_name_database):
                break
        for r in reader:
            send_data_to_api(r)


def read_and_send_file_xlsx(arg1_file_name, arg2_name_database):
    rd = xlrd.open_workbook(arg1_file_name)
    sheet = rd.sheet_by_index(0)
    for rownumb in range(1, sheet.nrows):
        r = sheet.row_values(rownumb)
        if detect_all_cell_numb(r, arg2_name_database, sheet, rd, rownumb):
            break
    for rownumb in range(1, sheet.nrows):
        r = sheet.row_values(rownumb)
        if sheet.cell(rownumb, dict_numb_cell['data']).ctype == 3:  # xldate
            send_data_to_api(r, rd)
        else:
            send_data_to_api(r)


def send_data_to_api(arg1_data_row, arg2_rd=None):
    if '@' in arg1_data_row[dict_numb_cell['mail']]:
        mail = arg1_data_row[dict_numb_cell['mail']]


        if dict_numb_cell['data'] == '000':
            data = datetime.datetime.today().strftime(('%Y-%m-%d'))
            print(data)
        elif arg2_rd != None:
            year, month, day, hour, minute, second = xlrd.xldate_as_tuple(arg1_data_row[dict_numb_cell['data']], arg2_rd.datemode)
            data = str(datetime.date(year, month, day))
        else:
            if re.findall('^\d{2}.\d{2}.\d{4}$', str(arg1_data_row[dict_numb_cell['data']])):
                temp_date = str(arg1_data_row[dict_numb_cell['data']]).split('.')
                data = temp_date[2]+'-'+temp_date[1]+'-'+temp_date[0]
            elif re.findall('^\d{2}.\d{2}.\d{2}$', str(arg1_data_row[dict_numb_cell['data']])):
                temp_date = str(arg1_data_row[dict_numb_cell['data']]).split('.')
                data = '20'+temp_date[2]+'-'+temp_date[1]+'-'+temp_date[0]
            elif re.findall('^\d{4}-\d{2}-\d{2}$', str(arg1_data_row[dict_numb_cell['data']])):
                data = arg1_data_row[dict_numb_cell['data']]
            else:
                data = datetime.datetime.today().strftime(('%Y-%m-%d'))


        if dict_numb_cell['name'] == '000' or arg1_data_row[dict_numb_cell['name'] ] == '':
            name = 'Matt'
        else:
            name = arg1_data_row[dict_numb_cell['name']]


        if dict_numb_cell['transaction'] == '000' or arg1_data_row[dict_numb_cell['transaction'] ] == '':
            transaction = str(time.time())
        else:
            transaction = arg1_data_row[dict_numb_cell['transaction']]
        post_data = {
            "Token": token,
            "Orders":
                [
                    {
                        "ID": transaction,
                        "BuyerName": name,
                        "BuyerEmail": mail,
                        "DeliveryDate": data},
                    {
                        "ID": "OrderIDWithProducts",
                        "BuyerName": "Some Buyer Name 2",
                        "BuyerEmail": "some2@buyer.email",
                        "DeliveryDate": "2018-05-20",
                        "Products":
                            [
                                {
                                    "SKU": "12qa26",
                                    "Name": "some product",
                                    "Url": "some product url"
                                },
                                {
                                    "SKU": "12qa256",
                                    "Name": "some product 2",
                                    "Url": "some product url 2"
                                }
                            ]
                    }
                ]
        }

        headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla'}
        print(post_data)
        # exit()
        # post = requests.post(url, json.dumps(post_data).encode('UTF-8'), headers=headers)

    else:
        pass


def __main__():
    name_database = []
    with open('Names_DataBase', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            name_database.append(row[1].lower().strip())

    file_name = easygui.fileopenbox(filetypes=["*.*"])
    if '.xlsx' in file_name or '.xls' in file_name:
        print('its .xlsx or .xls format')
        read_and_send_file_xlsx(file_name, name_database)

    elif '.csv' in file_name:
        print('its .csv format')
        read_and_send_file_csv(file_name, name_database)

    else:
        print('format is not correct')


dict_numb_cell = {}
url = ''
token = ''
__main__()
