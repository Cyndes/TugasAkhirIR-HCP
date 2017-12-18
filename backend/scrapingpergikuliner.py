# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import sys
import string
import re

reload(sys)
sys.setdefaultencoding('utf-8')
#r_input = raw_input("masukkan nama restoran: ")
#r_input = "holycow steak"
# if len(r_input.split()) > 1:
# 	r_name = string.replace(r_input, ' ', '+')
# else:
# 	r_name = r_input

def search_pergikuliner(query):
	tmpurl = ("https://pergikuliner.com/restaurants?utf8=✓&search_place=&default_search=&search_name_cuisine={}".format(query))
	headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
	tmppage = requests.get(tmpurl, headers=headers)
	tmpcontent = tmppage.text
	tmpsoup = BeautifulSoup(tmpcontent, 'html.parser')
	pages = tmpsoup.find('h2', id='top-total-search-view')
	if pages:
		pages = pages.get_text().strip()
		pattern = re.compile(r'[0-9]+')
		pages = re.findall(pattern, pages)[1]
		pages = ((int(pages)/12) / 15) + 1
	else:
		pages = 0

	search_result = {}
	if pages > 5:
		pages = 5
	count = 1
	while count <= pages:
		tmpcontent = requests.get("https://pergikuliner.com/restaurants?default_search=jakarta&page="+ str(count) +"&search_name_cuisine="+ query +"&search_place=", 
			headers=headers).text
		soup = BeautifulSoup(tmpcontent, 'html.parser')
		for data, rat, img in zip(soup.find_all('div', class_="item-info"), soup.find_all('div', class_='item-rating-result'), soup.find_all('img', class_='main-img')):
			details = {}
			name = data.find('h3', class_="item-name").get_text().strip()
			alamat = data.find('p', class_="clearfix").find_all('span', class_='truncate')
			alamat = ", ".join([Alamat.get_text().encode("utf-8").strip() for Alamat in data.find('p', class_="clearfix").find_all('span', class_='truncate')])
			rating = float(rat.get_text().strip().split('/')[0])
			details['alamat'] = alamat
			details['rating'] = round(rating * 2, 2)
			details['review'] = 0
			details['image'] = img.get('src')
			search_result[name + " - " + re.sub('Mall | Mall|mall | mall', "", alamat.split(",")[0])] = details
		count += 1
	return search_result


def see_details_pergikuliner(name):	
	#print "inputnya sekarang jadi " + r_name
	#url = "https://pergikuliner.com/restaurants?utf8=✓&search_place=&default_search=Jakarta&search_name_cuisine=cafe"
	tmpurl = ("https://pergikuliner.com/restaurants?search_place="+ name.split("-")[1].strip() +"&default_search=&search_name_cuisine="+ name.split("-")[0].strip())
	headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
	tmppage = requests.get(tmpurl, headers=headers)
	tmpcontent = tmppage.text
	soup = BeautifulSoup(tmpcontent, 'html.parser')
	if "Hasil cari" in soup.title.string:
		links = soup.find_all('a', href=True)
		url = "https://pergikuliner.com" + links[33]['href']
		page = requests.get(url, headers=headers)
		content = page.text
		soup = BeautifulSoup(content, 'html.parser')


	place = soup.find_all(itemprop="name")
	province = place[1].string
	city = place[2].string
	street = place[3].string
	address = soup.find("article").find("p").find("span").get_text().strip()
	ratingOverall = soup.find(itemprop = "ratingValue").string #rating
	cuisine = soup.find(itemprop = "servesCuisine").string #jenis restoran
	telephone = soup.find(itemprop = "telephone").find("a").string #no telfon
	pricerange = soup.find(itemprop = "priceRange").string.strip() #range harga
	openhours = soup.find(itemprop = "openingHours").string #waktu buka
	payment = soup.find(itemprop = "paymentAccepted") #jenis pembayaran
	hasfacilities = soup.find_all(class_ = "checked") #list fasilitas
	notfacilities = soup.find_all(class_ = "unchecked") #list bukan fasilitas
	recommenu = soup.find(class_ = "tbody").find_all("a") #recommended menu, tp yg keluar masih top reviewer aja


	# print "alamat " + address;
	# print province + " " + city + " " + street;
	# print "rating " + ratingOverall;
	# print "cuisine " + str(cuisine);
	# print "no telfon " + telephone;
	# print "range harga " + pricerange;
	# print "jam buka " + openhours;
	# print "pembayaran " + payment['content'];

	facilities = []
	for f in hasfacilities:
	   facilities.append(f.string);
	nofacilities = []
	# for nf in notfacilities:
	#    notfacilities.append(nf.string);

	details = {}
	# details["name"] = name.split("-")[0].strip()
	# details["address"] = address + " " + province + " " + city + " " + street
	details["rating"] = float(ratingOverall)
	details["telephone"] = telephone
	# details["review"] = int()
	# details["avg_cost"] = data[i]["restaurant"]["average_cost_for_two"]
	# details["facilities"] = ""
	# details["waktu_makan"] = waktu_makan
	# details["pemesanan_terakhir"] = ""
	# details["waktu_tunggu"] = ""
	# details["libur"] = ""
	# details["category"] = category
	# details["kapasitas"] = kapasitas
	# details["petunjuk_arah"] = petunjuk_arah
	# details["description"] = description
	# details["recommended_menu"] = recommended_menu
	# details["cuisine"] = data[i]["restaurant"]["cuisines"]
	details["opening_hours"] = openhours
	details["payment"] = payment['content']
	details["facilities"] = facilities
	# details["notfacilities"] = nofacilities
	return details

	#for m in recommenu:
	#   print m.string;

	# related restaurant by location
	# baseurlloc = "https://pergikuliner.com/restaurants?utf8=✓&search_place="+ street + "&default_search=&search_name_cuisine="
	# pageloc = requests.get(baseurlloc, headers=headers)
	# contentloc = pageloc.text
	# souploc = BeautifulSoup(contentloc, 'html.parser')

	# restolists = souploc.find_all(class_="item-info")

	# print "list of restaurants related to " + r_input + " based on location:";
	# for rl in restolists:
	# 	print rl.find("a").string + " " + rl.find_all("div")[1].string.strip();


	# related restaurant by food
	# baseurlfood = "https://pergikuliner.com/restaurants?utf8=✓&search_place=&default_search=&search_name_cuisine=" + cuisine
	# pagefood = requests.get(baseurlfood, headers=headers)
	# contentfood = pagefood.text
	# soupfood = BeautifulSoup(contentfood, 'html.parser')

	# restolists2 = soupfood.find_all(class_="item-info")
	# print "\n";
	# print "list of restaurants related to " + r_input + " based on cuisine:";
	# for rl2 in restolists2:
	# 	print rl2.find("a").string + " " + rl2.find_all("div")[1].string.strip();
# print search_restaurant(r_name)