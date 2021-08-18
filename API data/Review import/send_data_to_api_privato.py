import requests
import csv
import time
import json


##company_name = input('Введите имя компании, на которую оставили отзывы: ').strip()
##answer_email = input('Введите email компании, с которого будут опубликованы комментарии к отзывам: ').strip()



headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla'}
api_url = 'https://api.collect-reviews.com/v1.3/clients/57734A68-72C3-418D-BDAF-F2BD83EFE06D/reviews/Merchant'
# api_url = 'https://api.collect-reviews.com/v1.3/clients/6DC4450D-95CB-441D-B50B-9E3255FE8C86/reviews/Merchant'
# api_url(PROD) = 'https://api.collect-reviews.com/v1.3/clients/0185DC03-37C5-4806-B7C4-B8BF46E0F2A3/reviews/Merchant'
# api_url = 'https://api.collect-reviews.com/v1.3/clients/1FCBAE1D-1C2E-4E29-B43F-3A23ECFE4B36/reviews/Merchant'

token = 'ShXX%Y)C@KN@4@1r'
# token = '9s(Guq=WEScEHwfQ'
# token(PROD) = 'NmRlfo*wjp%6-Faq'
# token = 'QHoJ_2_RlUQ.oe!A'




while True:
    try:
        with open('ReviewsExport.csv', 'r', encoding='utf8', newline='') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader)
            for row in reader:




##                fake_mail = str(time.time()) + '@gmail.com'
##                if int(row[4]) <= 2:
##                    recommend = "false"
##                else:
##                    recommend = "true"

##                if row[2] == '':
##                    post_data ={
##                        "Token": token,
##                        "AuthorName": row[3],
##                        "AuthorEmail": fake_mail,
##                        "ReviewText": row[1],
##                        "Rate": row[4],
##                        "Date": row[5],
##                        "Recommends": recommend,
##                        "Meta":
##                            {
##                                "some rating": 5,
##                                "some text": "test",
##                                "some dropdown": "option 1",
##                                "some text area": "some text area text"
##                            },
##                    }
##                else:
                post_data ={
                    "Token": token,
                    "AuthorName": row[5],
                    "AuthorEmail": row[6],
                    "ReviewText": row[12],
                    "Rate": row[22],
                    "Date": row[21],
                    "Recommends": row[23],
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
                                "AuthorName": row[14],
                                "AuthorEmail": row[15],
                                "CommentText": row[19],
                                "Date": row[20]
                            },
                        ]}
                post = requests.post(api_url, json.dumps(post_data).encode('UTF-8'), headers = headers)
                print(json.dumps(post_data).encode('utf8'))
        print('Данные из файла "Review Collect.csv" были успешно отправлены')
        break

    except PermissionError:
        print('---------------Требуется закрыть файл "Review Collect.csv"!!!!!!!!!!!!!!!!!!------------------------')
        time.sleep(5)

