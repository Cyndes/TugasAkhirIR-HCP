import requests
import json
#from bs4 import BeautifulSoup
import re
import sys
import string

reload(sys)
sys.setdefaultencoding('utf-8')
r_input = raw_input("masukkan nama restoran: ")
r_name = string.replace(r_input, ' ', '%20')

def search_restaurant(query):
	url = ("https://developers.zomato.com/api/v2.1/search?entity_id=74&q={}".format(r_name))
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
		search_result[data[i]["restaurant"]["name"] + " - " + re.sub('Mall | Mall|mall | mall', "", details['alamat'].split(",")[0])] = details
	return search_result


def see_details(name):
	url = ("https://developers.zomato.com/api/v2.1/search?entity_id=74&q={}".format(r_name))

	headers = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": "6b2034187f3b4f96d476acff22f5bd49"}

	page = requests.get(url, headers=headers)
	restolist = json.loads(page.text)
	data = restolist["restaurants"]

	for i in range(0, 20):
		print data[i]["restaurant"]["name"] + " " + data[i]["restaurant"]["location"]["locality"] + " || rating: " + data[i]["restaurant"]["user_rating"]["aggregate_rating"];

#content = page.text
#soup = BeautifulSoup(content, 'html.parser')
print search_restaurant(r_name)


#print(soup.prettify())
