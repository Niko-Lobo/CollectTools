import requests
import json
import re
from random import choice
import time
import csv


def get_data(arg_http, arg_user, arg_proxi, arg_count):
	company_data = requests.get(arg_http, headers = arg_user, proxies = arg_proxi)
	json_str = re.findall('{ "@context" :.+} } ] }', company_data.text)[0]
	a = json.loads(json_str)
	name = a['name']
	link = a['url']
	try:
		company_phone = re.findall('<strong>Phone:<\/strong><br \/>.+', company_data.text)[0][29:]
	except IndexError:
		company_phone = ''
	try:
		company_email = re.findall('<strong>Email:<\/strong> <br \/>.+', company_data.text)[0][30:]
	except IndexError:
		company_email = ''
	try:
		rating = a['aggregateRating']['ratingValue']
		review_count = a['aggregateRating']['reviewCount']
	except IndexError:
		rating = 'no rating'
		review_count = 'no review'
	list_data = []
	list_data.append(name)
	list_data.append(link)
	list_data.append(company_phone)
	list_data.append(company_email)
	list_data.append(rating)
	list_data.append(review_count)
	print(arg_count, name, link, company_phone, company_email, rating, review_count)
	with open('Company_data.csv', 'a', encoding='cp1251', newline='') as f:
		writer = csv.writer(f, delimiter=';')
		writer.writerow(list_data)


link = 'https://www.reviews.co.uk/sitemap.xml'
r = requests.get(link)
http_list = re.findall('(https:\/\/www.reviews.co.uk\/company\-reviews\/store\/.+)<\/loc>', r.text)
count=1

with open('exception_log.txt', 'w') as log_file:
    log_file.close()

with open('Company_data.csv', 'a', encoding='cp1251', newline='') as f:
	writer = csv.writer(f, delimiter=';')
	header = [ 'Company name', 'Domain name', 'Phone', 'Email', 'Rating', 'Total reviews']
	writer.writerow(header)



proxies = open('proxies.txt').read().strip().split('\n')
useragents = open('user_agent.txt').read().split('\n')


for http in http_list:
	# print(http)
	user = {'User-Agent': choice(useragents)}
	proxi = {'http': 'http://' + choice(proxies)}
	while True:
		time.sleep(4)
		# time.sleep(1.5)
		# print(user, proxi)
		if requests.get(http, headers=user, proxies=proxi).status_code == 200:
			try:
				get_data(http, user, proxi, count)
			except IndexError:
				with open('exception_log.txt', 'a') as log_file:
					log_file.write( 'no data in: '+ http + '\r\n')
				print(count, 'no data to scriping', http)
			break
		else:
			print(http, ' site block me, status:'+ str(requests.get(http, headers=user, proxies=proxi).status_code) +' i will change proxi, and try one more time' , proxi, user)
			user = {'User-Agent': choice(useragents)}
			proxi = {'http': 'http://' + choice(proxies)}
			time.sleep(10)
	count = count + 1
