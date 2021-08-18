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
        driver.find_element_by_id('nextbtn').click()
        time.sleep(1)
        WebDriverWait(driver, max_time_out).until(EC.presence_of_element_located((By.ID, 'password')))
        driver.find_element_by_id('password').send_keys(password)
        driver.find_element_by_id('nextbtn').click()
    except SystemError:
        pass


def click_buttom_by_XPATH(arg_XPATH, arg_timeout):
    WebDriverWait(driver, arg_timeout).until(EC.element_to_be_clickable((By.XPATH, arg_XPATH)))
    time.sleep(1)
    print('i tried click',arg_XPATH)
    driver.find_element_by_xpath(arg_XPATH).click()


def choose_filter_for_robot():
    browser = driver.get("https://crm.zoho.eu/crm/org20078232582/tab/Contacts/custom-view/371001000000030971/list?filter_id=371001000000334005")


def open_company_in_general_table():
    time.sleep(1)
    Xpath_row_in_table = config['Button5']
    WebDriverWait(driver, max_time_out).until(EC.presence_of_element_located((By.XPATH, Xpath_row_in_table)))
    driver.find_element_by_xpath(Xpath_row_in_table).click()



def main(arg_1):
    if arg_1 == True:
        autorisation_step()
    else:
        pass
    choose_filter_for_robot()
    open_company_in_general_table()
    click_buttom_by_XPATH(Xpath_Button_Send, max_time_out)
    current_window = driver.current_window_handle
    new_window = driver.window_handles[1]
    driver.switch_to.window(new_window)
    click_buttom_by_XPATH(Xpath_Button_Template, max_time_out)

    click_buttom_by_XPATH(Xpath_button_Filter, max_time_out)
    click_buttom_by_XPATH(Xpath_button_Sendout, max_time_out)
    driver.switch_to.window(current_window)


# send_quantity = int(input('введите количество сообщений, которое необходимо отправить:').strip())
send_quantity = 1000
# numb_day_of_week = datetime.datetime.today().isoweekday()
numb_day_of_week = 6
config = {}
read_config()
work_url = config['URL']
list_data_row = []
numb_sucsess_send = 0
profine_numb = str(1) #input('введите номер профайла: '))
username = config['User' + profine_numb]
password = config['Password' + profine_numb]
max_time_out = config['max_time_out']
min_time_out = config['min_time_out']

Xpath_Button_Send = config['Button1']
Xpath_Button_Template = config['Button2']
Xpath_button_Filter = config['Button3']
Xpath_button_Sendout = config['Button4']
Xpath_button_Emails = config['Button6']
Xpath_button_Create_Emails = config['Button7']
Xpath_button_Sequences = config['Button8']
Xpath_Choose_Sequences = config['Button9']
Xpath_Button_Sendold = config['Button22']
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
            driver = webdriver.Chrome() #executable_path=path_Chrome)
            browser = driver.get(work_url)
            driver.maximize_window()
            first_run = True

driver.close()
print('Job Done')
