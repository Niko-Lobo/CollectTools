from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import time
import datetime
import xlrd

path_Chrome = '/usr/local/bin'


error_msg = 'There was a problem loading this next_page.'


def read_config():
    rd = xlrd.open_workbook('Config.xls')
    sheet = rd.sheet_by_index(0)
    for rownumb in range(1, sheet.nrows):
        row = sheet.row_values(rownumb)
        config[row[0]] = row[1]


def autorisation_step():
    try:
        WebDriverWait(driver, max_time_out).until(EC.presence_of_element_located((By.ID, 'login_id')))
        driver.find_element_by_id('login_id').send_keys(username)
        time.sleep(5)
        WebDriverWait(driver, max_time_out).until(EC.presence_of_element_located((By.ID, 'password')))
        driver.find_element_by_id('password').send_keys(password)
        driver.find_element_by_id('loginBtn').click()
    except SystemError:
        pass


def click_buttom_by_XPATH(arg_XPATH, arg_timeout):
    WebDriverWait(driver, arg_timeout).until(EC.element_to_be_clickable((By.XPATH, arg_XPATH)))
    time.sleep(1)
    print('i tried click',arg_XPATH)
    driver.find_element_by_xpath(arg_XPATH).click()


def choose_filter_for_robot():
    click_buttom_by_XPATH(Xpath_Button_Contact, max_time_out)
    click_buttom_by_XPATH(Xpath_Button_Companies, max_time_out)
    # print('i wait button all filter')
    click_buttom_by_XPATH(Xpath_button_All_Saved_Filters, max_time_out)
    click_buttom_by_XPATH(Xpath_filter_for_Robot, max_time_out)


def open_company_in_general_table():
    time.sleep(1)
    row = 1
    while True:

        Xpath_row_in_table = config['Button5']+str(row)+']'
        WebDriverWait(driver, max_time_out).until(EC.presence_of_element_located((By.XPATH, Xpath_row_in_table)))

        Xpath_current_mail_in_row = config['Button5']+str(row)+']'
        company_name = driver.find_element_by_xpath(Xpath_current_mail_in_row).text
        if company_name in list_data_row:
            row = row + 1
            # print('company name ' + company_name + ' is repit, i will take next row num ', row)
        else:
            current_email = driver.find_element_by_xpath(Xpath_current_mail_in_row).text
            list_data_row.append(current_email)
            driver.find_element_by_xpath(Xpath_row_in_table).click()
            break


def select_sequences(arg_1):
    #if arg_1 == True:
    #     click_buttom_by_XPATH(Xpath_Choose_Sequences, max_time_out)
    #     WebDriverWait(driver, max_time_out).until(EC.visibility_of_element_located((By.CLASS_NAME, 'Select-option')))
    #     driver.find_element_by_class_name('Select-option').click()
    # else:
    #     pass
 #   click_buttom_by_XPATH(Xpath_button_Templates_selector, max_time_out)
 #   click_buttom_by_XPATH(Xpath_button_All_templates, max_time_out)

    # select = Select(driver.find_element_by_css_selector("#uiabstractdropdown-button-91 > span > span.private-dropdown__button-label.uiDropdown__buttonLabel"))
    # select.select_by_value("All")


    sequience_choise = ''
    while sequience_choise != 'Best WOO Plugin2':
        WebDriverWait(driver, max_time_out).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.table-row-cell-hover')))
        all_sequiences = driver.find_elements_by_css_selector('.table-row-cell-hover')
        for sequience in all_sequiences:
            if 'Best WOO Plugin2' in sequience.text:
                sequience_choise = 'Best WOO Plugin2'
                sequience.click()
                break
        if sequience_choise != 'Best WOO Plugin2':
            click_buttom_by_XPATH(config['Button10'],
                                  min_time_out)
        else:
            break


def change_company_status():
    # click_buttom_by_XPATH(Xpath_company_status, max_time_out)
    # WebDriverWait(driver, min_time_out).until(EC.visibility_of_element_located((By.CLASS_NAME, 'Select-option')))
    # all_status = driver.find_elements_by_class_name('Select-option')
    # for status in all_status:
    #     if status.text == 'Pre-qualified':
    #         status.click()
    #         break
    #     else:
    #         pass
    # # -Click Save--
    # WebDriverWait(driver, min_time_out).until(EC.visibility_of_element_located((By.CLASS_NAME, 'UniversalSaveBar')))
     time.sleep(0.5)
    # driver.find_element_by_class_name('UniversalSaveBar').find_element_by_tag_name('button').click()


def click_send_now():
    # WebDriverWait(driver, min_time_out).until(
    #     EC.presence_of_all_elements_located((By.CLASS_NAME, 'sequence-enroll-modal-footer')))
    time.sleep(1)
    # driver.find_element_by_class_name('sequence-enroll-modal-footer').find_element_by_tag_name('button').click()
    click_buttom_by_XPATH(Xpath_Button_Send, min_time_out)


def main(arg_1):
    if arg_1 == True:
        autorisation_step()
        time.sleep(30)
        choose_filter_for_robot()
    else:
        pass
    open_company_in_general_table()
    click_buttom_by_XPATH(Xpath_button_Emails, max_time_out)
    click_buttom_by_XPATH(Xpath_button_Create_Emails, max_time_out)

    # ---click sequences---
    WebDriverWait(driver, max_time_out).until(EC.element_to_be_clickable((By.XPATH, Xpath_button_Sequences,)))
    time.sleep(1)
    driver.find_element_by_xpath(Xpath_button_Sequences, ).click()
    # try:
    #     WebDriverWait(driver, 30).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, '.table-row-cell-hover')))
    # except exceptions.TimeoutException:
    #     driver.find_element_by_xpath(Xpath_button_Sequences, ).click()
    # # ---------------------
    select_sequences(arg_1)
    # --click "SEND-MAIL"--
    try:
        click_send_now()

    except exceptions.WebDriverException:
        msg = driver.find_element_by_tag_name('h4').text
        if error_msg == msg:
            print('its error on site(maybe company didnt have mail in contact)' + str(msg))
            click_buttom_by_XPATH(config['Button12'], min_time_out)
        elif msg == "Team can't be enrolled in this sequence":
            print('This contact is already enrolled in a sequence')
            click_buttom_by_XPATH(config['Button12'], min_time_out)
    # --mail was send--
    try:
        change_company_status()
    except exceptions.WebDriverException:
        pass
    click_buttom_by_XPATH(Xpath_button_Back_to_Contacts, max_time_out)


# send_quantity = int(input('введите количество сообщений, которое необходимо отправить:').strip())
send_quantity = 1000
# numb_day_of_week = datetime.datetime.today().isoweekday()
numb_day_of_week = 6
config = {}
read_config()
work_url = config['URL']
list_data_row = []
numb_sucsess_send = 0
profine_numb = str(2) #input('введите номер профайла: '))
username = config['User' + profine_numb]
password = config['Password' + profine_numb]
max_time_out = config['max_time_out']
min_time_out = config['min_time_out']

Xpath_Button_Contact = config['Button1']
Xpath_Button_Companies = config['Button2']
Xpath_button_All_Saved_Filters = config['Button3']
Xpath_filter_for_Robot = config['Button4']
Xpath_button_Emails = config['Button6']
Xpath_button_Create_Emails = config['Button7']
Xpath_button_Sequences = config['Button8']
Xpath_Choose_Sequences = config['Button9']
Xpath_Button_Send = config['Button22']
Xpath_button_Templates_selector = config['Button20']
Xpath_button_All_templates = config['Button14']
Xpath_company_status = config['Button15']

Xpath_button_Back_to_Contacts = config['Button16']


driver = webdriver.Chrome()
driver.maximize_window()
browser = driver.get(work_url)

first_run = True
while numb_sucsess_send < send_quantity:
    try:
        main(first_run)
        first_run = False
        numb_sucsess_send = numb_sucsess_send + 1
        print('mail numb ' + str(numb_sucsess_send) + ' was send')

    except exceptions.WebDriverException:
        try:
            msg = driver.find_element_by_tag_name('h1').text
            if msg == "You've reached the limit.":
                print(msg)
                break
            else:
                pass
        except exceptions.WebDriverException:
            driver.close()
            print('now i will wait 60 sec after exception error',exceptions.WebDriverException)
            time.sleep(5)
            driver = webdriver.Chrome(executable_path=path_Chrome)
            browser = driver.get(work_url)
            driver.maximize_window()
            first_run = True

driver.close()
print('Job Done')