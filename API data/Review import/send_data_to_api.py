import requests
import csv
import time
import json


company_name = input('Введите имя компании, на которую оставили отзывы: ').strip()
answer_email = input('Введите email компании, с которого будут опубликованы комментарии к отзывам: ').strip()



headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla'}
api_url = 'https://api.collect-reviews.com/v1.3/clients/448E9D1A-635F-43F5-929B-65E68A956A6E/reviews/Merchant'

token = '*XDp^-;_k*7X}9>-'




while True:
    try:
        with open('Copy of Reviews (2).csv', 'r', encoding='utf8', newline='') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)
            for row in reader:




                fake_mail = str(time.time()) + '@gmail.com'
                if int(row[3]) <= 2:
                    recommend = "false"
                else:
                    recommend = "true"

                if row[2] == '':
                    post_data ={
                        "Token": token,
                        "AuthorName": row[4],
                        "AuthorEmail": row[6],
                        "ReviewText": row[1],
                        "Rate": row[3],
                        "Date": row[5],
                        "Recommends": recommend,
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
                        "AuthorName": row[4],
                        "AuthorEmail": fake_mail,
                        "ReviewText": row[1],
                        "Rate": row[3],
                        "Date": row[5],
                        "Recommends": recommend,
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
                                    "Date": "2018-09-06T14:57:22"
                                },
                            ]}
                post = requests.post(api_url, json.dumps(post_data).encode('UTF-8'), headers = headers)
                print(json.dumps(post_data).encode('utf8'))
        print('Данные из файла "Review Collect.csv" были успешно отправлены')
        break

    except PermissionError:
        print('---------------Требуется закрыть файл "Review Collect.csv"!!!!!!!!!!!!!!!!!!------------------------')
        time.sleep(5)

