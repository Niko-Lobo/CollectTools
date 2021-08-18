from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import time

work_url = 'https://app.hubspot.com/contacts/3908475/contacts/list/view/all/?'
url_with_filter = 'https://app.hubspot.com/contacts/3908475/contacts/list/view/2372391/?'
username = 'kate@collect-reviews.co.uk'
password = 'GetThingsDone!'
max_time_out = 100
min_time_out = 50
row = 1

Xpath_buttom_All_Saved_Filters = '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div/div[1]/div/div[1]/nav/ul/li[2]/a/span/button/span/i18n-string'
Xpath_filter_for_Robot = '/html/body/div[2]/div/div/div[2]/div/div/div[2]/div/div[2]/div/div[3]/div/nav/ul/li[1]/a/span/span'
Xpath_buttom_Emails = '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div[1]/div/a[3]/i18n-string'
Xpath_buttom_Create_Emails = '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div[2]/div[1]/button[2]/i18n-string'
Xpath_buttom_Templates = '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div[2]/div/div/div/div/div/div[1]/ul/li[1]/button/i18n-string'
Xpath_Choose_Templates = '/html/body/div[6]/div/div/div/div/div/div/div[2]/div/div[1]/div/div[1]/div/span/span[1]/span/span/span'
Xpath_buttom_Contacts = '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[1]/aside/section/div/div/div/div[1]/div/div[1]/nav/a/span/i18n-string'


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
    driver.find_element_by_xpath(arg_XPATH).click()


def choose_filter_for_robot():
    click_buttom_by_XPATH(Xpath_buttom_All_Saved_Filters, max_time_out)
    click_buttom_by_XPATH(Xpath_filter_for_Robot, max_time_out)


def open_company_in_general_table():
    row = 1
    while True:
        Xpath_row_in_table = '/html/body/div[2]/div/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/table/tbody/tr[' + str(
            row) + ']/td[2]/div/div[1]/span/span/span/div/a/span/span/span'
        WebDriverWait(driver, max_time_out).until(EC.presence_of_element_located((By.XPATH, Xpath_row_in_table)))

        Xpath_current_mail_in_row = '/html/body/div[2]/div/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/table/tbody/tr[' + str(
            row) + ']/td[3]/span/span/span/a'

        if driver.find_element_by_xpath(Xpath_current_mail_in_row).text in list_data_row:
            row = row + 1
        else:
            current_email = driver.find_element_by_xpath(Xpath_current_mail_in_row).text
            list_data_row.append(current_email)
            driver.find_element_by_xpath(Xpath_row_in_table).click()
            break
        print('all mail before is repit, i will take row num ', row)


def open_and_create_email(arg_first_run=False):
    click_buttom_by_XPATH(Xpath_buttom_Emails, max_time_out)
    click_buttom_by_XPATH(Xpath_buttom_Create_Emails, max_time_out)
    click_buttom_by_XPATH(Xpath_buttom_Templates, max_time_out)
    if arg_first_run == True:
        click_buttom_by_XPATH(Xpath_Choose_Templates, max_time_out)
        WebDriverWait(driver, max_time_out).until(EC.visibility_of_element_located((By.CLASS_NAME, 'Select-option')))
        driver.find_element_by_class_name('Select-option').click()
    else:
        pass

    x = 0
    while True:
        try:
            Xpath_buttom_Best_contact = '/html/body/div[' + str(
                x) + ']/div/div/div/div/div/div/div[2]/div/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/div/div[1]/span/span/span/a'
            driver.find_element_by_xpath(Xpath_buttom_Best_contact).click()
            break
        except exceptions.NoSuchElementException:
            x += 1
            if x == 30:
                x = 0
            else:
                pass

    time.sleep(3)
    driver.find_element_by_css_selector('.private-button--primary').click()

    click_buttom_by_XPATH(Xpath_buttom_Contacts, max_time_out)


def open_and_send_mail(arg_first_start):
    if arg_first_start == True:
        autorisation_step()
        choose_filter_for_robot()
    else:
        pass
    open_company_in_general_table()
    open_and_create_email(arg_first_start)


driver = webdriver.Chrome()
brauser = driver.get(work_url)
driver.maximize_window()
first_run = True

list_data_row = []
n = 0
while n <= 300:
    try:
        open_and_send_mail(first_run)
        first_run = False
        n += 1
        print('Mail numb', n, 'was send')
        if n // 50 == 0:
            print('TimeOut#1 now i will wait 60 sec, then i refresh next_page and filter for robot')
            driver.refresh(60)
            choose_filter_for_robot()
        else:
            pass
    except exceptions.WebDriverException:
        driver.close()
        print('now i will wait 60 sec, because i have exception, and i cant find some element')
        time.sleep(60)
        driver = webdriver.Chrome()
        brauser = driver.get(work_url)
        driver.maximize_window()
        first_run = True
        open_and_send_mail(first_run)
        first_run = False
        n += 1
driver.close()
print('im finish')
