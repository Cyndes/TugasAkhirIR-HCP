import json
import re
import requests
from bs4 import BeautifulSoup

def search_foody(query):
	# For accessing openrice search
	url = "www.foody.id/jakarta/places?q=" + query + "&ss=header_search_form"
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
				image = item['PhotoUrl']
				# ambil alamat sampe koma aja
				fixed_alamat = re.sub(',.*', "", alamat)
				# ilangin kata "mall"
				fixed_alamat = re.sub('Mall | Mall|mall | mall', "", fixed_alamat)
				fixed_name = re.sub(' -.*', "", name) + " - " + fixed_alamat

				if rating:
					details["rating"] = float(rating)
				else:
					details["rating"] = 0
				if review:
					details["review"] = int(review)
				else:
					details["review"] = 0				
				details["alamat"] = alamat
				details["image"] = image

				search_results[fixed_name] = details 
		elif " - " in name:
			alamat = food.find('span', "").find('span', "").string
			rating = food.find('div', class_="point highlight-text")
			image = food.findPreviousSiblings()[0].find("img").get("src")
			
			if rating:
				rating = rating.string.strip()
			review = food.find('a', href="javascript:void(0)").find('span', "").string
			# ambil alamat sampe koma aja
			fixed_alamat = re.sub(',.*', "", alamat)
			# ilangin kata "mall"
			fixed_alamat = re.sub('Mall | Mall|mall | mall', "", fixed_alamat)
			fixed_name = re.sub(' -.*', "", name) + " - " + fixed_alamat

			details['foody_name'] = name
			if rating:
				details["rating"] = float(rating)
			else:
				details["rating"] = 0
			if review:
				details["review"] = int(review)
			else:
				details["review"] = 0
			details["alamat"] = alamat
			details["image"] = image

			search_results[fixed_name] = details 
		else:
			alamat = food.find('span', "").find('span', "").string
			image = food.findPreviousSiblings()[0].find("img").get("src")
			rating = food.find('div', class_="point highlight-text")
			if rating:
				rating = rating.string.strip()
			review = food.find('a', href="javascript:void(0)").find('span', "").string
			# ambil alamat sampe koma aja
			fixed_alamat = re.sub(',.*', "", alamat)
			# ilangin kata "mall"
			fixed_alamat = re.sub('Mall | Mall|mall | mall', "", fixed_alamat)
			fixed_name = name + " - " + fixed_alamat

			if rating:
				details["rating"] = float(rating)
			else:
				details["rating"] = 0
			if review:
				details["review"] = review
			else:
				details["review"] = 0
			details["alamat"] = alamat

			search_results[fixed_name] = details 
	return search_results

def see_details_foody(name):
	url = "www.foody.id/jakarta/places?q=" + name + "&ss=header_search_form"
	headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
	r = requests.get("http://" + url, headers=headers)
	search = r.text

	soup = BeautifulSoup(search, 'html.parser')
	url = "www.foody.id"

	# Taking static data from the first result
	url += soup.find('h2').find('a').get('href')
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
	else:
		avg_rating = 0

	# review
	review = soup.find("div", class_="microsite-review-count")
	if review:
		review = review.string.strip()
	else:
		review = 0

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

	# description and recommended menu
	description = ""
	recommended_menu = ""
	x = 1
	for desc in soup.find('div', class_="special-content").find_all('li'):
		if x == 3:
			recommended_menu = desc.string
		
		description += desc.string + " "
		x += 1

	if ":" in recommended_menu:
		recommended_menu = re.search(':.*[^.]', recommended_menu).group(0)[2:] #ada yg ga pake ":"

	foody_details = {}
	foody_details["name"] = name
	foody_details["address"] = location
	foody_details["rating_foody"] = avg_rating
	foody_details["review_foody"] = review
	foody_details["avg_cost"] = avg_cost
	foody_details["facilities"] = facilities
	foody_details["waktu_makan"] = waktu_makan
	foody_details["pemesanan_terakhir"] = pemesanan_terakhir
	foody_details["waktu_tunggu"] = waktu_tunggu
	foody_details["libur"] = libur
	foody_details["category"] = category
	foody_details["kapasitas"] = kapasitas
	foody_details["petunjuk_arah"] = petunjuk_arah
	foody_details["description"] = description
	foody_details["recommended_menu"] = recommended_menu

	print foody_details
	return foody_details

restaurant = raw_input("Restaurants you want to find? ")
#search_foody(restaurant)
see_details_foody(restaurant)
