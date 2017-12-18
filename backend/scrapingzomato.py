import requests
import json
#from bs4 import BeautifulSoup
import re
import sys
import string

reload(sys)
sys.setdefaultencoding('utf-8')
# r_input = raw_input("masukkan nama restoran: ")
# r_name = string.replace(r_input, ' ', '%20')

def search_zomato(query):
	url = ("https://developers.zomato.com/api/v2.1/search?entity_id=74&q={}".format(query))
	headers = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": "6b2034187f3b4f96d476acff22f5bd49"}
	page = requests.get(url, headers=headers)
	restolist = json.loads(page.text)
	data = restolist["restaurants"]

	search_result = {}
	for i in range(0, 20):
		details = {}
		details['alamat'] = data[i]["restaurant"]["location"]["address"]
		details['review'] = int(data[i]["restaurant"]["user_rating"]["votes"])
		details['rating'] = float(data[i]["restaurant"]["user_rating"]["aggregate_rating"])
		details['image'] = data[i]["restaurant"]["featured_image"]
		search_result[data[i]["restaurant"]["name"] + " - " + re.sub('Mall | Mall|mall | mall', "", details['alamat'].split(",")[0])] = details
	return search_result


def see_details_zomato(name):
	url = ("https://developers.zomato.com/api/v2.1/search?entity_id=74&q={}".format(name))

	headers = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": "6b2034187f3b4f96d476acff22f5bd49"}

	page = requests.get(url, headers=headers)
	restolist = json.loads(page.text)
	data = restolist["restaurants"]

		print data[i]["restaurant"]["name"] + " " + data[i]["restaurant"]["location"]["locality"] + " || rating: " + data[i]["restaurant"]["user_rating"]["aggregate_rating"];

	details = {}
	for i in range(0, 20):
		if data[i]["restaurant"]["name"] == name.split("-")[0].strip():
			details["name"] = data[i]["restaurant"]["name"]
			details["address"] = data[i]["restaurant"]["location"]["address"]
			details["rating"] = float(data[i]["restaurant"]["user_rating"]["aggregate_rating"])
			details["review"] = int(data[i]["restaurant"]["user_rating"]["votes"])
			details["avg_cost"] = data[i]["restaurant"]["average_cost_for_two"]
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
			details["cuisine"] = data[i]["restaurant"]["cuisines"]
			# details["waktu_buka"] = waktu_buka
			break
	return details

#content = page.text
#soup = BeautifulSoup(content, 'html.parser')
#print search_restaurant(r_name)


#print(soup.prettify())
