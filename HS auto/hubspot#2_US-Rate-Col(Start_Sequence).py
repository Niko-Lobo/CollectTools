from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import time
import datetime
import xlrd

path_Chrome = './chromedriver'



error_msg = 'There was a problem loading this next_page.'


def read_config():
    rd = xlrd.open_workbook('Configure_US_R.xlsx')
    sheet = rd.sheet_by_index(0)
    for rownumb in range(1, sheet.nrows):
        row = sheet.row_values(rownumb)
        config[row[0]] = row[1]


def autorisation_step():
    try:
        WebDriverWait(driver, max_time_out).until(EC.presence_of_element_located((By.ID, 'username')))
        driver.find_element_by_id('username').send_keys(username)
        WebDriverWait(driver, max_time_out).until(EC.presence_of_element_located((By.ID, 'password')))
        driver.find_element_by_id('password').send_keys(password)
        driver.find_element_by_id('loginBtn').click()
    except SystemError:
        pass


def click_buttom_by_XPATH(arg_XPATH, arg_timeout):
    WebDriverWait(driver, arg_timeout).until(EC.element_to_be_clickable((By.XPATH, arg_XPATH)))
    time.sleep(0.5)
    # print('i try click')
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

        # Xpath_row_in_table = '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/table/tbody/tr[' + str(
        #     row) + ']/td[2]/div/div[1]/span/span/span/div/a/span/span/span'
        Xpath_row_in_table = config['Button5']+str(row)+']'
        WebDriverWait(driver, max_time_out).until(EC.presence_of_element_located((By.XPATH, Xpath_row_in_table)))

        # Xpath_current_mail_in_row = '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/table/tbody/tr[' + str(
        #     row) + ']/td[2]/div/div[1]/span/span/span/div/a/span/span'
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
    if arg_1 == True:
        click_buttom_by_XPATH(Xpath_Choose_Sequences, max_time_out)
        WebDriverWait(driver, max_time_out).until(EC.visibility_of_element_located((By.CLASS_NAME, 'Select-option')))
        driver.find_element_by_class_name('Select-option').click()
    else:
        pass
    sequience_choise = ''
    while sequience_choise != 'Bad Ratings - Collecting - US':
        WebDriverWait(driver, max_time_out).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.table-row-cell-hover')))
        all_sequiences = driver.find_elements_by_css_selector('.table-row-cell-hover')
        for sequience in all_sequiences:
            if 'Bad Ratings - Collecting - US' in sequience.text:
                sequience_choise = 'Bad Ratings - Collecting - US'
                sequience.click()
                break
        if sequience_choise != 'Bad Ratings - Collecting - US':
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
     time.sleep(1)
    # driver.find_element_by_class_name('UniversalSaveBar').find_element_by_tag_name('button').click()


def click_send_now():
    WebDriverWait(driver, min_time_out).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'sequence-enroll-modal-footer')))
    driver.find_element_by_class_name('sequence-enroll-modal-footer').find_element_by_tag_name('button').click()
    # click_buttom_by_XPATH(Xpath_Button_Send, min_time_out)


def main(arg_1):
    if arg_1 == True:
        autorisation_step()
        choose_filter_for_robot()
    else:
        pass
    open_company_in_general_table()
    click_buttom_by_XPATH(Xpath_button_Emails, max_time_out)
    click_buttom_by_XPATH(Xpath_button_Create_Emails, max_time_out)

    # ---click sequences---
    WebDriverWait(driver, max_time_out).until(EC.element_to_be_clickable((By.XPATH, Xpath_button_Sequences,)))
    driver.find_element_by_xpath(Xpath_button_Sequences, ).click()
    try:
        WebDriverWait(driver, 4).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.table-row-cell-hover')))
    except exceptions.TimeoutException:
        driver.find_element_by_xpath(Xpath_button_Sequences, ).click()
    # ---------------------
    select_sequences(arg_1)
    # --click "SEND-MAIL"--
    try:
        click_send_now()



        # if numb_day_of_week <= 5:
        #     click_send_now()
        # else:
        #     print('today is holiday')
        #     click_buttom_by_XPATH(config['Button13'], min_time_out)
        #     click_buttom_by_XPATH(config['Button14'], min_time_out)
        #     click_buttom_by_XPATH(config['Button17'], min_time_out)
        #     driver.find_element_by_xpath("//input[@type='search']").send_keys(config['Time_start_sequences'])
        #     click_buttom_by_XPATH(config['Button18']+config['Time_start_sequences']+"']", min_time_out)
        #     driver.find_element_by_xpath(config['Button19']).click()
        #     driver.find_element_by_xpath(config['Button19']).click()
        #     driver.find_element_by_xpath(config['Button19']).clear()
        #     driver.find_element_by_xpath(config['Button19']).send_keys('17/06/2019')
            # click_send_now()

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
send_quantity = 200
# numb_day_of_week = datetime.datetime.today().isoweekday()
numb_day_of_week = 6
config = {}
read_config()
work_url = config['URL']
list_data_row = []
numb_sucsess_send = 0
profine_numb = str(input('введите номер профайла: '))
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
Xpath_company_status = config['Button15']

Xpath_button_Back_to_Contacts = config['Button16']


driver = webdriver.Chrome(executable_path=path_Chrome)
brauser = driver.get(work_url)
driver.maximize_window()
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
            print('now i will wait 60 sec after exception error')
            time.sleep(20)
            driver = webdriver.Chrome(executable_path=path_Chrome)
            brauser = driver.get(work_url)
            driver.maximize_window()
            first_run = True

driver.close()
print('im finish')
