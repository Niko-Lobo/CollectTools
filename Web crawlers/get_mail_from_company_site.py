import csv
import requests
from selenium import common
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
import easygui

link = 'https://www.thegamesupply.net/About_staff/'


def write_file(arg_data):
    with open('Correct_File.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(arg_data)


def settings():
    list_old_file = []
    file_for_read = easygui.fileopenbox(msg="Select CSV file", default="*.csv", filetypes='*.CSV')
    dict_settings = {'delimiter': ';', 'encoding': 'UTF-8', 'number cell with url': 0,
                     'number cell with mail': 3, 'interrupted process': list_old_file, 'file_path': file_for_read}

    if file_for_read is None:
        print('ERROR. You do not choose the files')
        exit()
    elif '.csv' not in file_for_read:
        print('ERROR. You can use only ".csv" file format')
        exit()
    change_settings = 'y'
    while change_settings != 'n':
        with open(file_for_read, 'r', encoding=dict_settings['encoding']) as f:
            excel_File = csv.reader(f, delimiter=dict_settings['delimiter'])
            numb_row = 0
            print(
                '__________________________________________________PreView File____________________________________________________')
            for row in excel_File:
                numb_row += 1
                # print(len(row))
                if numb_row == 6:
                    break
                elif len(row) == 0:
                    pass
                elif row[0].strip() == '' and row[1].strip() == '' and row[2].strip() == '' and row[3].strip() == '':
                    pass
                else:
                    print(' | '.join(row))

            print(
                '------------------------------------------------------------------------------------------------------------------')
        print(
            'DELIMITER="' + dict_settings['delimiter'] + '"    ENCODING="' + dict_settings[
                'encoding'] + '"    NUMBER CELL WITH URL(numbering from 1)="' + str(
                dict_settings['number cell with url'] + 1) + '"    NUMBER CELL WITH MAIL(numbering from 1)="' + str(
                dict_settings['number cell with mail'] + 1) + '"')

        print('---If you want continue interrupted process(with current settings), enter "Continue"---')
        change_settings = input('Do you wont change settings?(Y/N): ').lower().strip()

        if change_settings == 'n':
            pass

        elif change_settings == 'y':
            change_key = input('Witch setting do you want change?(enter name setting): ').lower().strip().replace(
                '(numbering from 1)', '')
            change_value = input('Enter new value setting: ')
            if change_key is None:
                print('ERROR. Your input can not be empty.')
                exit()
            elif change_key == 'number cell with url' or change_key == 'number cell with mail':
                change_value = int(change_value)
                dict_settings[change_key] = change_value
            elif change_key == 'delimiter' or change_key == 'encoding':
                change_value = str(change_value)
                dict_settings[change_key] = change_value
            else:
                print('ERROR. Your input is not correct.')

        elif change_settings == 'continue':
            change_settings = 'n'
            # dict_settings['start_from'] = int(input('Input number row from i should be continue '))
            old_file = 'Correct_File.csv'
            try:
                with open(old_file, 'r', encoding='UTF-8') as oldf:
                    excel_File = csv.reader(oldf, delimiter=';')
                    for row_oldf in excel_File:
                        # print(row_oldf)
                        if len(row_oldf) == 0:
                            pass
                        elif row_oldf[0].strip() == '' and row_oldf[1].strip() == '' and row_oldf[2].strip() == '' and \
                                row_oldf[3].strip() == '':
                            pass
                        else:
                            list_old_file.append(row_oldf)
            except FileNotFoundError:
                print('For continue interrupted process, need old file "Correct_File.csv" in current directory')
        else:
            print('ERROR. Your input is not correct. You can use only "n" or "y".')
            exit()
    return dict_settings


def get_mail(arg_link):
    driwer = webdriver.Chrome()
    brawser = driwer.get(arg_link)
    driwer.maximize_window()
    mail = ''
    for button in list_all_button_wariant:
        try:
            contacts_url = driwer.find_element_by_partial_link_text(button).get_attribute('href')
            page_html = requests.get(contacts_url)
            all_soup = BeautifulSoup(page_html.text, 'html.parser')
            temp_mail_list = re.findall('([a-z]+.\w[@]\w+.\w+\.\w+)', str(page_html.content).lower())
            for temp_mail in temp_mail_list:
                if temp_mail.split('@')[1] in contacts_url:
                    mail = temp_mail
                    break
            if mail != '':
                break
        except Exception:
            pass
        except common.exceptions.TimeoutException:
            pass
    driwer.close()
    return mail


def __main__():
    dict_settings = settings()
    if len(dict_settings['interrupted process']) > 10:
        pass
    else:
        with open('File_with_Append_mail.csv', 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            header = ['Domain name', 'Company name', 'Phone', 'First name', 'Last Name', 'Email', 'Total reviews',
                      'Rating',
                      'Provider certificate page link', 'Status', 'Vertical']
            writer.writerow(header)
    numb_row_for_search = 0
    numb_success_find = 0
    continue_from_row = 0

    with open(dict_settings['file_path'], 'r', encoding=dict_settings['encoding']) as f:
        excel_File = csv.reader(f, delimiter=dict_settings['delimiter'])

        for list_row in excel_File:
            list_input_file.append(list_row)

    if len(dict_settings['interrupted process']) != 0:
        last = dict_settings['interrupted process'][-1]
        n = 0
        for r in list_input_file:
            n += 1
            try:
                r.index(last[0])
                continue_from_row = n
                print('I will pass row: '+ ' | '.join(list_input_file[continue_from_row]))

                break
            except ValueError:
                pass

    for row in list_input_file[continue_from_row + 1:]:
        if len(row) > 2 and row[dict_settings['number cell with mail']] is not None and row[
            dict_settings['number cell with url']] is not None:
            cell_with_mail = row[dict_settings['number cell with mail']]
            cell_with_URL = row[dict_settings['number cell with url']]
            if cell_with_mail.strip() == '' and 'http' in cell_with_URL.strip():

                numb_row_for_search += 1
                search_mail = get_mail(cell_with_URL)
                if search_mail is not None and search_mail.strip() != '':
                    numb_success_find += 1
                    print(str(numb_success_find) + ' Success search mail ( ' + search_mail + ' )')
                    row[dict_settings['number cell with mail']] = search_mail
                else:
                    print(
                        'No data in site: ' + cell_with_URL + ' .It was attempt number ' + str(numb_row_for_search))


        elif len(row) == 1:
            print('ERROR. In "File.csv" use delimiter other, than ",". Try change it.')
        data_row_with_name = row
        write_file(data_row_with_name)


list_all_button_wariant = []
list_button = ['About', 'Contact', 'Us']
list_input_file = []
for word in list_button:
    list_all_button_wariant.append(word)
    list_all_button_wariant.append(word.lower())
    list_all_button_wariant.append(word.upper())

__main__()
