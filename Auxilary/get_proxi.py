from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions

# link = 'https://hidemyna.me/ru/proxy-list/?type=s5#list'
# link = 'https://hidemyna.me/ru/proxy-list/?maxtime=2000&type=s5#list'
link = 'https://hidemyna.me/ru/proxy-list/?maxtime=2000&type=s5&anon=34#list'

driver = webdriver.Chrome()
brauser = driver.get(link)
driver.maximize_window()
numb_row = 1
WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content-section"]/section[1]/div/table/tbody/tr[1]/td[1]')))
next_page = 2
with open('proxies.txt', 'w') as file:
    file.close()

while next_page != 10:
    try:
        XPATH_ip = '//*[@id="content-section"]/section[1]/div/table/tbody/tr[' + str(numb_row) + ']/td[1]'
        XPATH_port = '//*[@id="content-section"]/section[1]/div/table/tbody/tr[' + str(numb_row) + ']/td[2]'
        ip = driver.find_element_by_xpath(XPATH_ip).text
        port = driver.find_element_by_xpath(XPATH_port).text
        numb_row += 1
        data = ip + ':' + port
        with open('proxies.txt', 'a') as file:
            file.write(data + '\n')
        print(data)
    except exceptions.NoSuchElementException:
        next_page += 1
        numb_row = 1
        XPATH_page = '//*[@id="content-section"]/section[1]/div/div[4]/ul/li[' + str(next_page) + ']/a'
        try:
            driver.find_element_by_xpath(XPATH_page).click()
        except exceptions.NoSuchElementException:
            driver.close()
            exit()