import json
import re
import requests
from bs4 import BeautifulSoup
restaurant = raw_input("Restaurants you want to find? ")


def search_result(query):
    # For accessing openrice search
    url = "id.openrice.com/en/jakarta/restaurants?what="+restaurant
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    r = requests.get("http://" +url, headers=headers)
    search = r.text

    soup = BeautifulSoup(search, 'html.parser')
    url = "id.openrice.com"

    #Getting number of pages
    page = int(soup.find('div', class_="js-dishFilter").find('li').get('data-count'))
    page = (page / 15) + 1

    #Getting all result to map
    search_result = {}
    count = 1
    while count <= page:
        url = "id.openrice.com/en/jakarta/restaurants?what="+restaurant+"&page="+str(count)
        r = requests.get("http://" +url, headers=headers)
        search = r.text
        soup = BeautifulSoup(search, 'html.parser')
        for a in soup.find_all('li', class_='pois-restaurant-list-cell'):
            details = {}
            name = a.find('h2', class_='title-name').get_text().strip()
            if not name:
                name = ""
            alamat = a.find('div', class_='address')
            if not alamat:
                alamat = ""
            else:
                details['alamat'] = alamat.find('span').get_text().strip()
                alamat = alamat.find('span').get_text().split(',')[0].strip()
            review = a.find('div', class_='counters-container')
            if not review:
                review = 0
            else:
                review = int(re.findall(re.compile(r'[0-9]+'), review.find('span').get_text())[0])
            details['review'] = review
            good = a.find('div', class_='smile-face')
            rating = 0
            if good:
                good = int(good.find('span').get_text())
                bad = int(a.find('div', class_='sad-face').find('span').get_text())
                ok = review - good + bad
                rating = round(((7.5 * good) + (5 * ok) + (2.5 * bad))/review, 1)
            details['rating'] = rating
            search_result[name + " - " + alamat] = details

        count = count + 1
    return search_result

def detail_query(name):
    # For accessing openrice detail from search hit
    name = name.split('-')
    url = "id.openrice.com/en/jakarta/restaurants?what="+name[0].strip()+"&where="+name[1].strip()
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    r = requests.get("http://" +url, headers=headers)
    search = r.text
    soup = BeautifulSoup(search, 'html.parser')
    url = "http://id.openrice.com"
    data = soup.find('li', class_='pois-restaurant-list-cell')
    if not data:
        return "N/A"
    url += data.find('a').get('href')
    soup = BeautifulSoup (r.text, 'html.parser')
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

    script = soup.find('script', type='application/ld+json')
    if script:
        data = json.loads(script.text)

        #Getting address data
        data_add = data['address']
        address = data_add['streetAddress']+" "+data_add['addressLocality']+" "+data_add['addressRegion']+" "+data_add['postalCode']
        print address.encode("utf-8")

        #Getting telephone
        telephone = data['telephone']
        print telephone.encode("utf-8")

    facilities = []
    for avail_facil in soup.find_all('div', class_='condition-item'):
        if avail_facil.find('span', class_='or-sprite-inline-block d_sr2_lhs_tick_desktop'):
            facilities.append(avail_facil.find('span', class_='condition-name').string)
    print facilities

    rating = soup.find('div', class_='header-score-details-left-score', itemprop='ratingValue')
    print rating
    
print search_result(restaurant)