import json
import re
import requests
from bs4 import BeautifulSoup
restaurant = raw_input("Restaurants you want to find? ")

# For accessing openrice search
url = "id.openrice.com/en/jakarta/restaurants?what="+restaurant
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
r = requests.get("http://" +url, headers=headers)

search = r.text

soup = BeautifulSoup(search, 'html.parser')
url = "id.openrice.com"
url_detail = []

#Looping through all available link in openrice
page = int(soup.find('div', class_="js-dishFilter").find('li').get('data-count'))
page = (page / 15) + 1

for 
for link in soup.find_all('h2', class_='title-name'):
    url_detail.append(link.find('a').get('href'))

print url_detail

# for link in url_detail:
#     r = requests.get("http://" +url, headers=headers)

# data = r.text
# soup = BeautifulSoup(search, 'html.parser')

# data = json.loads(soup.find('script', type='application/ld+json').text)
# name = data['name']
# print name
# data_add = data['address']
# address = data_add['streetAddress']+" "+data_add['addressLocality']+" "+data_add['addressRegion']+" "+data_add['postalCode']
# print address
# telephone = data['telephone']
# print telephone
# cost = data['priceRange']
# pattern = re.compile(r'([0-9]+).([0-9]+)')
# avg_cost = 0
# for (ribuan, ratusan) in re.findall(pattern, cost):
#     avg_cost += int(ribuan+""+ratusan)

# avg_cost /= 2
# print avg_cost

# facilities = []
# for avail_facil in soup.find_all('div', class_='condition-item'):
# 	if avail_facil.find('span', class_='or-sprite-inline-block d_sr2_lhs_tick_desktop'):
# 		facilities.append(avail_facil.find('span', class_='condition-name').string)

# print facilities

# sign_dish = []	
# for sign_dishes in soup.find('section', class_='signature-dishes-section').find('div', class_='slash-tags'):
# 	sign_dish.append(sign_dishes.string.strip())

# sign_dish = filter(None, sign_dish)
# print sign_dish

# rating = soup.find('div', class_='header-score-details-left-score', itemprop='ratingValue').string.strip()
# print rating

# jenis = soup.find('meta', property='og:description').get('content')
# jenis_resto = []
# pattern = re.compile(r'[a-zA-Z]+')
# for x in re.findall(pattern, jenis):
#     jenis_resto.append(x)

# def filterReviews(element):
# 	return element != "reviews"

# jenis_resto = filter(filterReviews, jenis_resto)
# print jenis_resto

