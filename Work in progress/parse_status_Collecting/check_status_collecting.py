import csv
import easygui
import selenium
from selenium import webdriver
from selenium import common
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def read_file():
    file_path = easygui.fileopenbox()
    with open(file_path, 'r', encoding='UTF-8',) as f:
        reader = csv.reader(f, delimiter=',')
        data = []
        next(reader)
        for string in reader:
            data.append(string)
    return data


def write_file(arg1_file_result, arg2_str_old_file, arg3_company_status, arg4_attempt):
    with open(arg1_file_result, 'a', encoding='UTF-8', newline='') as nf:
        writer = csv.writer(nf, delimiter=';')
        string = []
        string.append(arg2_str_old_file[0])
        string.append(arg2_str_old_file[1])
        string.append(arg2_str_old_file[2])
        string.append(arg3_company_status)
        writer.writerow(string)
        print('Success attempt numb ' + str(arg4_attempt) + ' data: '+' , '.join(string))


def main():
    numb = 1
    file_result = input('Input Name file-result :').strip().replace('/', '_').replace(':','_').replace('.','_')+'.csv'
    file = read_file()
    for company in file:
        company_URL = company[2]
        try:
            driver = webdriver.Chrome()
            brauser = driver.get(company_URL)
            driver.maximize_window()
            XPATH_status = '//section[2]/div/div[1]/div/div/div[1]/span'
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, XPATH_status)))
            company_status = driver.find_element_by_xpath(XPATH_status).text
            XPATH_advertising = '/html/body/main/div/div[4]/aside/div[3]/ins'
            if company_status.strip() == 'Asking for reviews' :
                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, XPATH_advertising)))
                    company_status = 'collecting-FREE'
                except selenium.common.exceptions.TimeoutException:
                    company_status = 'collecting-PAID'
            elif company_status.strip() == 'Claimed':
                company_status = 'claimed(last_status_collecting)'
            else:
                company_status = 'unknown'
            write_file(file_result, company, company_status, numb)
            numb += 1
        except Exception:
            print('Attempt numb: ' + str(numb) + ' is FAIL ' + company_URL)
            company_status = 'error'
            write_file(file_result, company, company_status, numb)
            numb += 1
        finally:
            driver.close()
main()