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

#Getting number of pages
url_detail = []
page = int(soup.find('div', class_="js-dishFilter").find('li').get('data-count'))
page = (page / 15) + 1

#Taking static data from the first result
url += soup.find('h2', class_='title-name').find('a').get('href')
r = requests.get("http://"+url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

#Taking name data
data = json.loads(soup.find('script', type='application/ld+json').text)
name = data['name'] #Save name
print name

cost = data['priceRange']   #Save average cost
pattern = re.compile(r'([0-9]+).([0-9]+)')
avg_cost = 0
for (ribuan, ratusan) in re.findall(pattern, cost):
    avg_cost += int(ribuan+""+ratusan)

avg_cost /= 2
print avg_cost

jenis = soup.find('meta', property='og:description').get('content') #Save restaurant type
jenis_resto = []
pattern = re.compile(r'[a-zA-Z]+')
for x in re.findall(pattern, jenis):
    jenis_resto.append(x)

def filterReviews(element):
  return element != "reviews"

jenis_resto = filter(filterReviews, jenis_resto)
print jenis_resto

sign_dish = []
dish = soup.find('section', class_='signature-dishes-section')
if dish:
    dish = dish.find('div', class_='slash-tags')
    for sign_dishes in dish:
        sign_dish.append(sign_dishes.string.strip())

sign_dish = filter(None, sign_dish)
print sign_dish

#Looping through all available link in openrice
count = 1
while count <= page:
    url = "id.openrice.com/en/jakarta/restaurants?what="+restaurant+"&page="+str(count)
    r = requests.get("http://" +url, headers=headers)
    search = r.text
    soup = BeautifulSoup(search, 'html.parser')
    for link in soup.find_all('h2', class_='title-name'):
        url_detail.append(link.find('a').get('href'))
    count += 1
    
# print url_detail

#Looping through all url to get data
address_branch = []
telephone_branch = []
facility_branch = []
rating_branch = []

for link in url_detail:
    r = requests.get("http://id.openrice.com" +link, headers=headers)

    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    script = soup.find('script', type='application/ld+json')
    if script:
        data = json.loads(script.text)

        #Getting address data
        data_add = data['address']
        address = data_add['streetAddress']+" "+data_add['addressLocality']+" "+data_add['addressRegion']+" "+data_add['postalCode']
        address_branch.append(address)
        #print address.encode("utf-8")

        #Getting telephone
        telephone = data['telephone']
        telephone_branch.append(telephone)
        #print telephone.encode("utf-8")
    else:
        address_branch.append("None")
        telephone_branch.append("None")

    facilities = []
    for avail_facil in soup.find_all('div', class_='condition-item'):
    	if avail_facil.find('span', class_='or-sprite-inline-block d_sr2_lhs_tick_desktop'):
    		facilities.append(avail_facil.find('span', class_='condition-name').string)
    facility_branch.append(facilities)
    #print facilities

    rating = soup.find('div', class_='header-score-details-left-score', itemprop='ratingValue')
    if rating:
        rating_branch.append(rating.string.strip())
        #print rating.string.strip()
    else:
        rating_branch.append('0')

print address_branch
print telephone_branch
print facility_branch
print rating_branch