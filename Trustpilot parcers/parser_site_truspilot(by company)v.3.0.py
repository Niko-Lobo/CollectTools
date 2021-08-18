import requests
from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver
from selenium import common
import csv
from random import choice
import datetime


# ----------------------------------------work(parse) with open next_page----------------------------------------------------

def ip():
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
    while True:
        time.sleep(3)
        try:
            n = 0
            while True:
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
                get_data.append(company_status[8:])
                dict_url_company[company_url] = get_data
                with open('Url_Company.csv', 'a', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f, delimiter=';')
                    get_data.append(company_url)
                    writer.writerow(get_data)
        except common.exceptions.NoSuchElementException:
            try:
                url_next_page = driver.find_elements_by_partial_link_text('Next next_page')[0].get_attribute("href")
                driver.get(url_next_page)
            except IndexError:
                print(len(dict_url_company))
                print(
                    'All next_page with company url in sub-categories ' + category_name + company_status + ' is parse(exception#1)')
                driver.close()
                return False
        except common.exceptions.UnexpectedAlertPresentException:
            print(len(dict_url_company))
            print(
                'All next_page with company url in sub-categories ' + category_name + company_status + ' is parse(exception#2)')
            driver.close()
            return False


def get_url_page_for_parse(status, arg_site):

    list_all_category = get_category_url(arg_site)
    for sub_category_url in list_all_category:
        url_categories = arg_site + sub_category_url + status
        print('start parse category' + sub_category_url + status)
        get_company_url(url_categories, sub_category_url, status)


def read_file_Url_Company():
    with open('Url_Company.csv', 'r', encoding='cp1251', newline='') as f:
        reader = csv.reader(f, delimiter=';')
        for r in reader:
            l = []
            l.append(r[0])
            l.append(r[1])
            l.append(r[2])
            dict_url_company[r[3]] = l


list_status = ['?status=claimed', '?status=unclaimed', '?status=collecting']

numb = 1
input_name = input('Введите имя нового файлa, который будет содержать сканированные данные(Дата добавится автоматически):')


exist_file = input_name + datetime.date.today().strftime('%d%b%Y')+'.csv'
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
    site = input('Введите ссылку для парсинга в формате "https://www.trustpilot.com/categories":').strip()
    with open('Url_Company.csv', 'w', encoding='utf-8', newline='') as f:
        create_file = csv.writer(f, delimiter=';')
    for status in list_status:
        get_url_page_for_parse(status, site)
elif mode == 'continue':
    read_file_Url_Company()
    print(dict_url_company)
else:
    print('Invalid mode')
    exit()

for url, vertical in dict_url_company.items():
    parse_page(url, exist_file, vertical[0], vertical[1], vertical[2], numb)
    numb = numb + 1
print('Насяльника,Моя закончить работа!')
