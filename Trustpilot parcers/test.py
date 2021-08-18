import requests
from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import common
import csv
from random import choice
import datetime

def get_company_url(link, category_name, company_status):
    driver = webdriver.Chrome()
    brauser = driver.get(link)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div[2]/section/div/div/div[1]/div/div')))
    try:
        count_of_resalt = int(driver.find_element_by_xpath('/html/body/main/div/div[2]/section/div/div/div[1]/div/div').text.split(' ', 1)[0])
    except ValueError:
        count_of_resalt = 1


    # time.sleep(3)
    n = 0
    m = 0

    if count_of_resalt == 0:
        print('Company in this status do not created')
        driver.close()
        return False

    while count_of_resalt > m:
        try:
            m = m + 1
            n = n + 1
            pattern = '\"domain' + str(n) + '\"'
            xpath = '//*[@id=' + pattern + ']/a'
            company_data = driver.find_element_by_xpath(xpath)
            company_url = company_data.get_attribute("href")
            vertical = driver.find_element_by_xpath('/html/body/main/div/div[1]/div/h1').text
            rating = driver.find_element_by_xpath(xpath + '/div/div[1]/div[3]').text
            get_data = []
            get_data.append(vertical)
            get_data.append(rating)
            if company_status.split('=')[-1] == '0':
                get_data.append('collected')
                # print('collected')
            else:
                # print(company_status.split('=')[-1])
                get_data.append(company_status.split('=')[-1])
            print('Data was added: '+company_url+' - '+ get_data[2])
            dict_url_company[company_url] = get_data
            # with open('Url_Company.csv', 'a', encoding='utf-8', newline='') as f:
            #     writer = csv.writer(f, delimiter=';')
            #     get_data.append(company_url)
            #     writer.writerow(get_data)

        except common.exceptions.NoSuchElementException:
            try:
                url_next_page = driver.find_elements_by_partial_link_text('Next page')[0].get_attribute("href")
                print('run to next page: ' + url_next_page)
                n = 0
                m = m - 1
                driver.close()
                driver = webdriver.Chrome()
                brauser = driver.get(url_next_page)
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="domain1"]')))

                # time.sleep(2)

            except IndexError:
                print('All next_page with company url in sub-categories ' + category_name + company_status + ' is parse(exception#1)')
                driver.close()
                return False
        except common.exceptions.UnexpectedAlertPresentException:
            print('All next_page with company url in sub-categories ' + category_name + company_status + ' is parse(exception#2)')
            driver.close()
            return False
    print('General count detected company is: ' + str(len(dict_url_company)))
    driver.close()


dict_url_company = {}

get_company_url('https://uk.trustpilot.com/categories/horseback_riding_service?numberofreviews=0&timeperiod=0&status=claimed', '/horseback_riding_service', '?numberofreviews=0&timeperiod=0&status=claimed')
