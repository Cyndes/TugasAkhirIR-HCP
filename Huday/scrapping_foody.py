import json
import re
import requests
from bs4 import BeautifulSoup

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
			url += food.find('a').get('href')
			r = requests.get("http://"+url, headers=headers)
			soup = BeautifulSoup(r.text, 'html.parser')
			
			tes = soup.find_all('script', type="text/javascript")[11].renderContents()
			tes = re.search('{.*};', tes).group(0)
			data = json.loads(tes[0:len(str(tes))-1])
			
			for item in data['Items']:
				name = item['Name']
				alamat = item['Address']
				rating = item['AvgRatingText']
				review = item['TotalReviews']
				fixed_name = re.search('(.*) - ', name).group(1) + " - " + alamat

				details["rating"] = rating
				details["review"] = review
				details["alamat"] = alamat

				search_results[fixed_name] = details 

				print "Nama Restoran: " + name
				print "Nama Restoran Fixed: " + fixed_name
				print "Rating: " + str(rating)
				print "Jumlah Review: " + str(review)
				print "Alamat: " + alamat
				print
		elif " - " in name:
			alamat = food.find('span', "").find('span', "").string
			rating = food.find('div', class_="point highlight-text")
			if rating:
				rating = rating.string.strip()
			review = food.find('a', href="javascript:void(0)").find('span', "").string
			fixed_name = re.search('(.*) - ', name).group(1) + " - " + alamat

			details["rating"] = rating
			details["review"] = review
			details["alamat"] = alamat

			search_results[fixed_name] = details 

			print "Nama Restoran: " + name
			print "Nama Restoran Fixed: " + fixed_name
			print "Rating: " + str(rating)
			print "Jumlah Review: " + review
			print "Alamat: " + alamat
			print
		else:
			alamat = food.find('span', "").find('span', "").string
			rating = food.find('div', class_="point highlight-text")
			if rating:
				rating = rating.string.strip()
			review = food.find('a', href="javascript:void(0)").find('span', "").string
			fixed_name = name + " - " + alamat

			details["rating"] = rating
			details["review"] = review
			details["alamat"] = alamat

			search_results[fixed_name] = details 

			print "Nama Restoran: " + name
			print "Nama Restoran Fixed: " + fixed_name
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

	# info tambahan
	waktu_makan = ""
	pemesanan_terakhir = ""
	waktu_tunggu = ""
	libur = ""
	kategori = ""
	kapasitas = ""
	petunjuk_arah = ""
	for x in soup.find_all('div', class_="new-detail-info-area"):
		keyname = x.find('a', class_="resinfo-report").get('errorkeyname')
		if keyname == 'Waktu Makan':
			waktu_makan = x.find('span').string
		elif keyname == 'Pemesanan terakhir':
			pemesanan_terakhir = x.find('div', "").text.strip()
		elif keyname == 'Waktu tunggu':
			waktu_tunggu = x.find('span').string.strip()
		elif keyname == 'Libur':
			libur = x.find('span').string
		elif keyname == 'Kategori':	
			category = x.find('a').string
		elif keyname == 'Kapasitas':
			kapasitas = x.find('span').string
		elif keyname == 'Petunjuk arah':
			petunjuk_arah = x.find('b').string	

	# description
	description = ""
	recommended_menu = ""
	x = 1
	for desc in soup.find('div', class_="special-content").find_all('li'):
		if x == 3:
			recommended_menu = desc.string
		
		description += desc.string + " "
		x += 1

	# recommended menu
	if ":" in recommended_menu:
		recommended_menu = re.search(':.*[^.]', recommended_menu).group(0)[2:] #ada yg ga pake ":"

	print "Nama Restoran: " + name 
	print "Alamat: " + location
	print "Average Cost: " + str(avg_cost)
	print "Rating: " + str(avg_rating)
	print "Fasilitas: " + str(facilities)
	print "Jam Operasional: " + waktu_makan
	print "Pemesanan Terakhir: " + pemesanan_terakhir
	print "Waktu Tunggu: " + waktu_tunggu
	print "Libur: " + libur
	print "Kategori: " + category
	print "Kapasitas: " + kapasitas
	print "Petunjuk Arah: " + petunjuk_arah
	print "Deskripsi: " + description
	print "Rekomendasi Menu: " + recommended_menu

restaurant = raw_input("Restaurants you want to find? ")
#print search_restaurant(restaurant)
see_details(restaurant)
