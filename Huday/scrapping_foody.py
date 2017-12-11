from bs4 import BeautifulSoup
import re

with open("foody.html") as fp:
	soup = BeautifulSoup(fp, 'html.parser')

# location
address = soup.find("span", itemprop="streetAddress").string
city = soup.find("span", itemprop="addressLocality").string
province = soup.find("span", itemprop="addressRegion").string

location = address + ", " + city + ", " + province

#print location

# average cost
cost = str(soup.find("span", itemprop="priceRange").find("span"))
pattern = re.compile(r'([0-9]+).([0-9]+)')
avg_cost = 0

for (ribuan, ratusan) in re.findall(pattern, cost):
    avg_cost += int(ribuan+""+ratusan)

avg_cost = avg_cost / 2.0

# rating
avg_rating = soup.find("div", class_="microsite-point-avg").string

#print avg_rating

# facilities
facilities = []
for facility in soup.find_all('a', style="float:left;padding:3px 0 0 5px;font-weight:bold;"):
	facilities.append(facility.string)

#print facilities

# jenis restoran
kategori = ""
for x in soup.find_all('div', class_="new-detail-info-area"):
	tes = x.find('a', errorkeyname="Kategori")
	if tes:
		kategori = x.find('a').string

#print kategori

# description
description = ""
menu = ""
x = 1
for desc in soup.find('div', class_="special-content").find_all('li'):
	if x == 3:
		menu = desc.string
	
	description += desc.string
	x += 1

print description

# recommended menu
recommended_menu = re.search(':.*[^.]', menu).group(0)[2:]

print recommended_menu