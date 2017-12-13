# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import sys
import string

reload(sys)
sys.setdefaultencoding('utf-8')
r_input = raw_input("masukkan nama restoran: ")
#r_input = "holycow steak"
if len(r_input.split()) > 1:
	r_name = string.replace(r_input, ' ', '+')
else:
	r_name = r_input
	
#print "inputnya sekarang jadi " + r_name
#url = "https://pergikuliner.com/restaurants?utf8=✓&search_place=&default_search=Jakarta&search_name_cuisine=cafe"
tmpurl = ("https://pergikuliner.com/restaurants?utf8=✓&search_place=&default_search=&search_name_cuisine={}".format(r_name))
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
tmppage = requests.get(tmpurl, headers=headers)
tmpcontent = tmppage.text
tmpsoup = BeautifulSoup(tmpcontent, 'html.parser')
links = tmpsoup.find_all('a', href=True)

url = "https://pergikuliner.com" + links[33]['href']
page = requests.get(url, headers=headers)
content = page.text
soup = BeautifulSoup(content, 'html.parser')



#print(soup.prettify())
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

print "alamat " + address;
print province + " " + city + " " + street;
print "rating " + ratingOverall;
print "cuisine " + str(cuisine);
print "no telfon " + telephone;
print "range harga " + pricerange;
print "jam buka " + openhours;
print "pembayaran " + payment['content'];

print "punya fasilitas:";
for f in hasfacilities:
   print f.string;
print "gapunya fasilitas:";
for nf in notfacilities:
   print nf.string;
#for m in recommenu:
#   print m.string;

# related restaurant by location
baseurlloc = "https://pergikuliner.com/restaurants?utf8=✓&search_place="+ street + "&default_search=&search_name_cuisine="
pageloc = requests.get(baseurlloc, headers=headers)
contentloc = pageloc.text
souploc = BeautifulSoup(contentloc, 'html.parser')

restolists = souploc.find_all(class_="item-info")

print "list of restaurants related to " + r_input + " based on location:";
for rl in restolists:
	print rl.find("a").string + " " + rl.find_all("div")[1].string.strip();


# related restaurant by food
baseurlfood = "https://pergikuliner.com/restaurants?utf8=✓&search_place=&default_search=&search_name_cuisine=" + cuisine
pagefood = requests.get(baseurlfood, headers=headers)
contentfood = pagefood.text
soupfood = BeautifulSoup(contentfood, 'html.parser')

restolists2 = soupfood.find_all(class_="item-info")
print "\n";
print "list of restaurants related to " + r_input + " based on cuisine:";
for rl2 in restolists2:
	print rl2.find("a").string + " " + rl2.find_all("div")[1].string.strip();
