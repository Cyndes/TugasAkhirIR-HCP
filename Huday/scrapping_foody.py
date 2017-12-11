import re
import requests
from bs4 import BeautifulSoup

#with open("foody.html") as fp:
#	soup = BeautifulSoup(fp, 'html.parser')

restaurant = raw_input("Restaurants you want to find? ")

# For accessing openrice search
url = "www.foody.id/jakarta/places?q=" + restaurant + "&ss=header_search_form"
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
r = requests.get("http://" + url, headers=headers)
search = r.text

soup = BeautifulSoup(search, 'html.parser')
url = "www.foody.id"

#Taking static data from the first result
url += soup.find('div', class_='resname').find('a').get('href')
r = requests.get("http://"+url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

url = "www.foody.id" + soup.find('div', class_="ldc-item-img").find('a').get('href')
r = requests.get("http://"+url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

# name
name = soup.find("h1", itemprop="name").string

print name 

# location
address = soup.find("span", itemprop="streetAddress").string
city = soup.find("span", itemprop="addressLocality").string
province = soup.find("span", itemprop="addressRegion").string

location = address + ", " + city + ", " + province

print location

# average cost
cost = str(soup.find("span", itemprop="priceRange").find("span"))
pattern = re.compile(r'([0-9]+).([0-9]+)')
avg_cost = 0

for (ribuan, ratusan) in re.findall(pattern, cost):
    avg_cost += int(ribuan+""+ratusan)

avg_cost = avg_cost / 2

print avg_cost

# rating
avg_rating = soup.find("div", class_="microsite-point-avg").string

print avg_rating

# facilities
facilities = []
for facility in soup.find_all('a', style="float:left;padding:3px 0 0 5px;font-weight:bold;"):
	facilities.append(facility.string)

print facilities

# jenis restoran
category = ""
for x in soup.find_all('div', class_="new-detail-info-area"):
	tes = x.find('a', errorkeyname="Kategori")
	if tes:
		category = x.find('a').string

print category

# description
description = ""
menu = ""
x = 1
for desc in soup.find('div', class_="special-content").find_all('li'):
	if x == 3:
		menu = desc.string
	
	description += desc.string + " "
	x += 1

print description

# recommended menu
recommended_menu = re.search(':.*[^.]', menu).group(0)[2:]

print recommended_menu