from bs4 import BeautifulSoup
import requests
import re
import csv
import time
import json

url = str(input('введите полную ссылку компании на сайте trustpilot для сбора отзывов(в конце можно добавить пробел) :')).strip()

page = ''
n = 1
full_link = url + page
try :
    r = requests.get(url)
except requests.exceptions.MissingSchema:
    print ('Введенная ссылка :"'+url+'" содержит ошибку. Проверьте правильность ее написания!!!')
    url = str(input('введите полную ссылку компании на сайте trustpilot для сбора отзывов(в конце можно добавить пробел) :')).strip()
    r = requests.get(url)
    full_link = url + page


# print(answer_email)

while True:
    try :
        with open('Review Collect.csv', 'w', encoding='utf8', newline='', ) as file:
            writer = csv.writer(file, delimiter=';')
            header = ['Title', 'Review', 'Replay', 'Name', 'Rating', 'DateTime']
            writer.writerow(header)
            break
    except PermissionError:
        print('---------------Требуется закрыть файл "Review Collect.csv"!!!!!!!!!!!!!!!!!!------------------------')
        time.sleep(5)

soup = BeautifulSoup(r.text, 'html.parser')
all_review_card = soup.select('.review-card')
#all_review_card = soup.select('.review-card xh-highlight')

try:
    answer_email = re.findall('"email":"(.*?)"', r.text)[0]
except IndexError:
    answer_email = 'no@email.com'
company_name = soup.select_one('.multi-size-header__big').getText()


while full_link == r.url:

    for review_card in all_review_card:
        # print('-----------------------------------------------------------------------')
        review_title = review_card.select_one('.review-content__title').text.strip()
        try:
            comment = review_card.select_one('.review-content__text').text.strip()
        except AttributeError:
            comment = "No comments"
        person_name = review_card.select_one('.consumer-information__name'). text.strip()
        date_time = str(re.findall('"publishedDate":"(.+)",',review_card.select_one('.review-content-header__dates').find('script').text))
        date_time = str(date_time[2:21])
        # print(review_card)
        if re.search('5 stars', str(review_card)) != None:
            rating = '5'
        elif re.search('4 stars', str(review_card)) != None:
            rating = '4'
        elif re.search('3 stars', str(review_card)) != None:
            rating = '3'
        elif re.search('2 stars', str(review_card)) != None:
            rating = '2'
        elif re.search('1 star', str(review_card)) != None:
            rating = '1'
        else:
            rating = '5'
        try:
            replay = review_card.select_one('.brand-company-reply__content').text.strip()
        except AttributeError:
            replay = ''
        if review_title in comment:
            review_title = ''
        string = []
        string.append(review_title)
        string.append(comment)
        string.append(replay)
        string.append(person_name)
        string.append(rating)
        string.append(date_time)
        # exit()
        with open('Review Collect.csv', 'a', encoding='utf8', newline='', ) as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(string)
        # print(string)
    n = n + 1
    page = '?page='+str(n)
    full_link = url + page
    r = requests.get(full_link)
    soup = BeautifulSoup(r.text, 'html.parser')
    all_review_card = soup.select('.review-card')
    print('start scan review on next_page numb ' +str(n))
    # print(review_title + comment + ' and answer ' + replay + ' P.S. '+person_name + str(date_time[0]) + rating)
print ('Сбор отзывов завершен. Результат находится в корневой папке данного исполняющего файла, под названием "Review Collect.csv"')
input('Для отправки отзывов в систему нажмите ENTER')


headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla'}
api_url = 'https://api.collect-reviews.com/v1.3/clients/3C65CBC4-E9C1-473A-ADF9-F6487D5EBF05/reviews/Merchant'
token = '>zuM*Z!br-@;q(/$'


while True:
    try:
        with open('Review Collect.csv', 'r', encoding='utf8', newline='') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)
            for row in reader:
                fake_mail = str(time.time()) + '@gmail.com'
                if int(row[4]) <= 2:
                    recommend = "false"
                else:
                    recommend = "true"
                mytimedate = '2020-04-04T22:50:16'
                if row[2] == '':
                    post_data ={
                        "Token": token,
                        "AuthorName": row[3],
                        "AuthorEmail": fake_mail,
                        "ReviewText": row[1],
                        "Rate": row[4],
                        "Date": mytimedate,
                        "Recommends": recommend,
                        "IsApproved": "CL6uY6Ue",
                        "Meta":
                            {
                                "some rating": 5,
                                "some text": "test",
                                "some dropdown": "option 1",
                                "some text area": "some text area text"
                            },
                    }
                else:
                    post_data ={
                        "Token": token,
                        "AuthorName": row[3],
                        "AuthorEmail": fake_mail,
                        "ReviewText": row[1],
                        "Rate": row[4],
                        "Date": row[5],
                        "Recommends": recommend,
                        "IsApproved": "CL6uY6Ue",
                        "Meta":
                            {
                                "some rating": 5,
                                "some text": "test",
                                "some dropdown": "option 1",
                                "some text area": "some text area text"
                            },
                        "Comments":
                            [
                                {
                                    "AuthorName": company_name,
                                    "AuthorEmail": answer_email,
                                    "CommentText": row[2],
                                    "Date": row[5]
                                },
                            ]}
                if int(row[4]) > 2:
                    post = requests.post(api_url, json.dumps(post_data), headers = headers)
                print(post_data)
                # break
        print('Данные из файла "Review Collect.csv" были успешно отправлены')
        break

    except PermissionError:
        print('---------------Требуется закрыть файл "Review Collect.csv"!!!!!!!!!!!!!!!!!!------------------------')
        time.sleep(5)

