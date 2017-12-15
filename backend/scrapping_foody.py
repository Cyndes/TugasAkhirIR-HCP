import re
import requests
from bs4 import BeautifulSoup

#with open("foody.html") as fp:
#	soup = BeautifulSoup(fp, 'html.parser')

def search_restaurant(query):
	# For accessing openrice search
	url = "www.foody.id/jakarta/places?q=" + restaurant + "&ss=header_search_form"
	headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
	r = requests.get("http://" + url, headers=headers)
	search = r.text

	soup = BeautifulSoup(search, 'html.parser')
	url = "www.foody.id"

	search_results = {}
	details = {}

	for food in soup.find_all('div', class_="row-view-right"):
		name = food.find('a').string.strip()
		
		if "Brand" in name:
			alamat = "huaaah"
			url += food.find('a').get('href')
			r = requests.get("http://"+url, headers=headers)
			soup = BeautifulSoup(r.text, 'html.parser')

			#to do ubah json jadi data, rating dan review adanya di json nya
		elif " - " in name:
			name = re.search('(.*) - ', name).group(1)
			alamat = food.find('span', "").find('span', "").string
		else:
			alamat = food.find('span', "").find('span', "").string

		rating = food.find('div', class_="point highlight-text")
		if rating:
			rating = rating.string.strip()
		
		review = food.find('a', href="javascript:void(0)").find('span', "").string
		
		details["rating"] = rating
		details["review"] = review
		details["alamat"] = alamat

		search_results[name+" - "+alamat] = details 

		print "Nama Restoran: " + name
		print "Rating: " + str(rating)
		print "Jumlah Review: " + review
		print "Alamat: " + alamat
		print

	return search_results

def see_details(query):
	url = "www.foody.id/jakarta/places?q=" + restaurant + "&ss=header_search_form"
	headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
	r = requests.get("http://" + url, headers=headers)
	search = r.text

	soup = BeautifulSoup(search, 'html.parser')
	url = "www.foody.id"

	# Taking static data from the first result
	url += soup.find('h2').find('a').get('href')
	print url
	r = requests.get("http://"+url, headers=headers)
	soup = BeautifulSoup(r.text, 'html.parser')

	# name
	name = soup.find("h1", itemprop="name").string

	# location
	address = soup.find("span", itemprop="streetAddress").string
	city = soup.find("span", itemprop="addressLocality").string
	province = soup.find("span", itemprop="addressRegion").string

	location = address + ", " + city + ", " + province

	# average cost
	cost = str(soup.find("span", itemprop="priceRange").find("span"))
	pattern = re.compile(r'([0-9]+).([0-9]+)')
	avg_cost = 0

	for (ribuan, ratusan) in re.findall(pattern, cost):
	    avg_cost += int(ribuan+""+ratusan)

	avg_cost = avg_cost / 2

	# rating
	avg_rating = soup.find("div", class_="microsite-point-avg")
	if avg_rating:
		avg_rating = avg_rating.string.strip()

	# facilities
	facilities = []
	for facility in soup.find_all('a', style="float:left;padding:3px 0 0 5px;font-weight:bold;"):
		facilities.append(facility.string)

	# jenis restoran
	category = ""
	for x in soup.find_all('div', class_="new-detail-info-area"):
		tes = x.find('a', errorkeyname="Kategori")
		if tes:
			category = x.find('a').string

	# description
	description = ""
	menu = ""
	x = 1
	for desc in soup.find('div', class_="special-content").find_all('li'):
		if x == 3:
			menu = desc.string
		
		description += desc.string + " "
		x += 1

	# recommended menu
	#recommended_menu = re.search(':.*[^.]', menu).group(0)[2:] #ada yg ga pake ":"

	print "Nama Restoran: " + name 
	print "Alamat: " + location
	print "Average Cost: " + str(avg_cost)
	print "Rating: " + str(avg_rating)
	print "Fasilitas: " + str(facilities)
	print "Kategori: " + category
	print "Deskripsi: " + description
	#print "Rekomendasi Menu: " + recommended_menu

restaurant = raw_input("Restaurants you want to find? ")
#print search_restaurant(restaurant)
see_details(restaurant)