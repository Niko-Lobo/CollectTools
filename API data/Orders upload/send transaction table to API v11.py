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
        dict_numb_cell['customer mail'] = mail
        dict_numb_cell['transaction date'] = data
        dict_numb_cell['customer name'] = name
        dict_numb_cell['transaction id'] = transaction
        confirm = 'n'
        while confirm != 'y':
            print(file_type)
            print('-----------------------------------------------------------------')
            print('Сonfirm the definition of the fields below: \n')
            if dict_numb_cell['transaction id'] == '000':
                print('Transaction ID: None')
            else:
                print('Transaction ID: ' + str(arg1_row[dict_numb_cell['transaction id']]))
            print('Customer Mail: ' + str(arg1_row[dict_numb_cell['customer mail']]))
            if dict_numb_cell['customer name'] == '000':
                print('Customer Name: None')
            else:
                try:
                    print('Customer Name: ' + str(arg1_row[int(dict_numb_cell['customer name'][0])]) + str(
                        arg1_row[int(dict_numb_cell['customer name'][1])]))
                except TypeError:
                    print(dict_numb_cell['customer name'])
                    print('Customer Name: ' + str(arg1_row[dict_numb_cell['customer name']]))
            if dict_numb_cell['transaction date'] == '000':
                print('Transaction Date: None')
            else:
                print('Transaction Date: ' + str(arg1_row[dict_numb_cell['transaction date']]))
            print('-----------------------------------------------------------------')
            confirm = input('Its correct? (y/n):')
            if confirm == 'n':
                change_key = input('Enter fields-name, which we should change:').lower()
                if change_key.lower() == 'customer name':
                    double_cell = input('Do you want to connect two cells? (y/n): ')
                    if double_cell == 'y':
                        try:
                            print('\nPREVIEW LOADER FILE:')
                            print(arg1_row)
                            first_cell = int(input('Enter number cell, include First Name')) - 1
                        except ValueError:
                            print('Your input is not correct')
                            exit()
                        try:
                            second_cell = int(input('Enter number cell, include Second Name')) - 1
                        except ValueError:
                            print('Your input is not correct')
                            exit()
                        dict_numb_cell['customer name'] = [first_cell, second_cell]
                    elif double_cell == 'n':
                        try:
                            print('\nPREVIEW LOADER FILE:')
                            print(arg1_row)
                            change_value = int(input('\nEnter fields-number in preview, which we should set:'))
                            dict_numb_cell[change_key] = int(change_value) - 1
                        except ValueError:
                            dict_numb_cell[change_key] = '000'
                    else:
                        print('Incorrect choice')
                        exit()

                else:
                    print('\nPREVIEW LOADER FILE:')
                    print(arg1_row)

                    try:
                        change_value = int(input('\nEnter fields-number in preview, which we should set:'))
                        dict_numb_cell[change_key] = int(change_value) - 1
                    except ValueError:
                        dict_numb_cell[change_key] = '000'

            elif confirm == '':
                print('Your input is not correct')
                exit()
        return dict_numb_cell
    else:
        print('Incorrect delimiter')

def read_and_send_file_csv(arg1_file_name, arg2_name_database):
    with open(arg1_file_name, 'r', encoding='cp1251', newline='') as f:
        customer_delimiter = input('Enter delimiter, which use in csv file: ')
        reader = csv.reader(f, delimiter=customer_delimiter)
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
        try:
            if sheet.cell(rownumb, dict_numb_cell['transaction date']).ctype == 3:  # xldate
                send_data_to_api(r, rd)
            else:
                send_data_to_api(r)
        except TypeError:
            send_data_to_api(r, rd)


def send_data_to_api(arg1_data_row, arg2_rd=None):
    if '@' in arg1_data_row[dict_numb_cell['customer mail']]:
        mail = arg1_data_row[dict_numb_cell['customer mail']]

        if dict_numb_cell['transaction date'] == '000':
            data = datetime.datetime.today().strftime(('%Y-%m-%d'))
            # print(data)
        elif arg2_rd != None:
            year, month, day, hour, minute, second = xlrd.xldate_as_tuple(
                arg1_data_row[dict_numb_cell['transaction date']], arg2_rd.datemode)
            data = str(datetime.date(year, month, day))
        else:
            if re.findall('^\d{2}.\d{2}.\d{4}$', str(arg1_data_row[dict_numb_cell['transaction date']])):
                temp_date = str(arg1_data_row[dict_numb_cell['transaction date']]).split('.')
                data = temp_date[2] + '-' + temp_date[1] + '-' + temp_date[0]
            elif re.findall('^\d{2}.\d{2}.\d{2}$', str(arg1_data_row[dict_numb_cell['transaction date']])):
                temp_date = str(arg1_data_row[dict_numb_cell['transaction date']]).split('.')
                data = '20' + temp_date[2] + '-' + temp_date[1] + '-' + temp_date[0]
            elif re.findall('^\d{4}-\d{2}-\d{2}$', str(arg1_data_row[dict_numb_cell['transaction date']])):
                data = arg1_data_row[dict_numb_cell['transaction date']]
            else:
                data = datetime.datetime.today().strftime(('%Y-%m-%d'))
        if type(dict_numb_cell['customer name']) == list:
            name = arg1_data_row[dict_numb_cell['customer name'][0]] + ' ' + arg1_data_row[dict_numb_cell['customer name'][1]]
        else:
            if dict_numb_cell['customer name'] == '000' or arg1_data_row[dict_numb_cell['customer name']] == '':
                name = 'Matt'
            else:
                name = arg1_data_row[dict_numb_cell['customer name']]

        if dict_numb_cell['transaction id'] == '000' or arg1_data_row[dict_numb_cell['transaction id']] == '':
            transaction = str(time.time())
        else:
            transaction = arg1_data_row[dict_numb_cell['transaction id']]
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
        post = requests.post(url, json.dumps(post_data).encode('UTF-8'), headers=headers)

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
        global file_type
        file_type = '.xlsx'

        # print('its .xlsx or .xls format')
        read_and_send_file_xlsx(file_name, name_database)

    elif '.csv' in file_name:
        file_type = '.csv'
        # print('its .csv format')
        read_and_send_file_csv(file_name, name_database)

    else:
        print('format is not correct')


dict_numb_cell = {}
url = ''
token = ''
__main__()
