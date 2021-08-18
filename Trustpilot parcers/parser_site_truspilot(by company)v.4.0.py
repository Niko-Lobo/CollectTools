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


# ----------------------------------------work(parse) with open next_page----------------------------------------------------

def ip(): #random proxi from the list
    proxy = {'http': 'http://' + choice(proxies)}
    return proxy


def user():
    useragent = {'User-Agent': choice(useragents)}
    return useragent


def get_html(link, useragent=None, proxy=None):
    try:
        r = requests.get(link, headers=useragent, proxies=proxy)
        print('use', useragent, proxy)
        return r
    except requests.exceptions.ConnectionError:
        print('Соединение разорвано, следующая попытка саеденения через 60 сек')
        time.sleep(60)
        r = requests.get(url, headers=useragent, proxies=proxy)
        print('use', useragent, proxy)
        return r


def get_text_data(soup, select_html_elem):
    try:
        return soup.select_one(select_html_elem).getText()
    except SystemError:
        print('not found')
    except AttributeError:
        return ' '


def get_content_data(pattern, string):
    try:
        return re.findall(pattern, str(string.content))[0]
    except IndexError:
        return ' '
    except SystemError:
        print('not found')


def parse_page(link, file_name, vertical, rating, arg_company_status, i):
    try:
        html_page = get_html(link, user(), ip())
        all_soup = BeautifulSoup(html_page.text, 'html.parser')
        company_name = get_text_data(all_soup, '.multi-size-header__big').strip().replace(';', ' , ')
        print('----------get company name')
        company_link = get_content_data('"url":"(.*?)"', html_page).strip().replace(';', ' , ')
        print('----------get company link')
        company_email = get_content_data('"email":"(.*?)"', html_page).strip().replace(';', ' , ')
        print('----------get company email')
        company_phone = get_content_data('"telephone":"(.*?)"', html_page).strip().replace(';', ' , ')
        try:
            company_reviews = re.findall('\n(.*?)\n', get_text_data(all_soup, '.header--inline'))[0].strip().replace(
                ';', ' , ')
        except IndexError:
            company_reviews = '0.0'
        print('----------get company reviews')
        company_status = arg_company_status.strip().replace(';', ' , ')
        print('----------get company status')
        try:
            company_vertical = re.findall('Best(.*)', vertical)[0].strip().replace(';', ' , ')
        except IndexError:
            company_vertical = vertical.strip().strip().replace(';', ' , ')
        print('----------get company vertical')
        company_rating = re.findall('([0-9].[0-9])', rating)[0].strip().replace(';', ' , ')
        print('----------get company rating')
        with open(file_name, 'a', encoding='utf-8', newline='', ) as file:
            writer = csv.writer(file, delimiter=';')
            string = []
            string.append(company_link)
            string.append(company_name)
            string.append(company_phone)
            string.append(company_email)
            string.append(company_reviews)
            string.append(company_rating)
            string.append(link)
            string.append(company_status)
            string.append(company_vertical)
            writer.writerow(string)
        print(i, ' data was add to file(' + file_name + '): ', string)

    except IndexError:
        pass


# ----------------------------------------------------------------------------------------------------------------------
def get_category_url(main_page_url):
    html_main_page = get_html(main_page_url, user(), ip()).text
    soup_main_page = BeautifulSoup(html_main_page, 'html.parser')
    return re.findall('href="\/categories(.*?)">', str(soup_main_page.select('.sub-category-item')))


def get_company_url(link, category_name, company_status):
    driver = webdriver.Chrome()
    brauser = driver.get(link)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div[2]/section/div/div/div[1]/div/div')))
        count_of_resalt = int(
            driver.find_element_by_xpath('/html/body/main/div/div[2]/section/div/div/div[1]/div/div').text.split(' ',
                                                                                                                 1)[0])
    except ValueError:
        count_of_resalt = 1
    except common.exceptions.TimeoutException:
        print('TimeOut Exception. Page with subcategory list do not loaded.')
        driver.close()
        return False
    except common.exceptions.UnexpectedAlertPresentException:
        print('Exception. UnexpectedAlertPresentException. I will close this subcategory')
        driver.close()
        return False

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
            print('Data was added: ' + company_url + ' - ' + get_data[2])
            dict_url_company[company_url] = get_data
            with open('Url_Company.csv', 'a', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, delimiter=';')
                get_data.append(company_url)
                writer.writerow(get_data)

        except common.exceptions.NoSuchElementException:
            try:
                url_next_page = driver.find_elements_by_partial_link_text('Next page')[0].get_attribute("href")
                print('run to next page: ' + url_next_page)
                n = 0
                m = m - 1
                driver.get(url_next_page)
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="domain1"]')))

                # time.sleep(2)

            except IndexError:
                print(
                    'All next_page with company url in sub-categories ' + category_name + company_status + ' is parse(exception#1)')
                driver.close()
                return False
            except common.exceptions.TimeoutException:
                print('TimeOut Exception. This subcategory i will pass')
                driver.close()
                return False
            except common.exceptions.UnexpectedAlertPresentException:
                print('Exception. UnexpectedAlertPresentException1. I will close this subcategory')
                driver.close()
                return False
        except common.exceptions.UnexpectedAlertPresentException:
            print(
                'All next_page with company url in sub-categories ' + category_name + company_status + ' is parse(exception#2)')
            driver.close()
            return False
        except Exception:
            print('Exception. I will close this subcategory')
            driver.close()
            return False

    print('General count detected company is: ' + str(len(dict_url_company)))
    driver.close()


def get_url_page_for_parse(arg_site=None):
    if arg_site == None:
        last_string = read_file_Url_Company()
        # print(type(last_string))
        arg_site = 'https://' + str(last_string[0].split('/')[2]) + '/categories'
        # print(site)
        all_category = get_category_url(arg_site)
        last_category = '/' + str(last_string[1].split(' ')[1].lower())
        n = 0
        for i in all_category:
            if last_category in i:
                break
            else:
                n += 1
        list_all_category = all_category[n:]
    else:
        list_all_category = get_category_url(arg_site)
    for sub_category_url in list_all_category:
        for status in list_status:
            url_categories = arg_site + sub_category_url + status
            print('start parse link ' + url_categories)
            get_company_url(url_categories, sub_category_url, status)


def read_file_Url_Company():
    with open('Url_Company.csv', 'r', encoding='cp1251', newline='') as f:
        reader = csv.reader(f, delimiter=';')
        last_str = []
        for r in reader:
            l = []
            l.append(r[0])
            l.append(r[1])
            l.append(r[2])
            dict_url_company[r[3]] = l
            last_str = [r[3], r[0], r[1], r[2]]
    return last_str


list_status = ['?numberofreviews=0&timeperiod=0&status=unclaimed', '?numberofreviews=0&timeperiod=0&status=claimed',
               '?numberofreviews=0&timeperiod=0']

numb = 1
input_name = input(
    'Введите имя нового файлa, который будет содержать сканированные данные(Дата добавится автоматически):')

exist_file = input_name + datetime.date.today().strftime('%d%b%Y') + '.csv'
mode = input('Enter mod, witch need use(default, continue): ').strip().lower()
dict_url_company = {}
proxies = open('proxies.txt').read().strip().split('\n')
useragents = open('user_agent.txt').read().split('\n')

with open(exist_file, 'w', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')
    header = ['Domain name', 'Company name', 'Phone', 'Email', 'Total reviews', 'Rating',
              'Provider certificate next_page link', 'Status', 'Vertical']
    writer.writerow(header)

if mode == 'default':
    resume = input('Continue append file(url company), or start new process?(yes/no): ').strip().lower()
    if resume == 'no':
        site = input('Введите ссылку для парсинга в формате "https://www.trustpilot.com/categories":').strip()
        with open('Url_Company.csv', 'w', encoding='utf-8', newline='') as f:
            create_file = csv.writer(f, delimiter=';')
        get_url_page_for_parse(site)
    elif resume == 'yes':

        get_url_page_for_parse()
    else:
        print('Incorrect input')
        exit()
elif mode == 'continue':
    read_file_Url_Company()
    print(dict_url_company)


elif mode == 'abroad':
    read_file_Url_Company()

else:
    print('Invalid mode')
    exit()

for url, vertical in dict_url_company.items():
    parse_page(url, exist_file, vertical[0], vertical[1], vertical[2], numb)
    numb = numb + 1
print('Насяльника,Моя закончить работа!')