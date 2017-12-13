import requests
import json
#from bs4 import BeautifulSoup
import sys
import string

reload(sys)
sys.setdefaultencoding('utf-8')
r_input = raw_input("masukkan nama restoran: ")
r_name = string.replace(r_input, ' ', '%20')
url = ("https://developers.zomato.com/api/v2.1/search?entity_id=74&q={}".format(r_name))

headers = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": "6b2034187f3b4f96d476acff22f5bd49"}

page = requests.get(url, headers=headers)
restolist = json.loads(page.text)
data = restolist["restaurants"]

for i in range(1, 19):
	print data[i]["restaurant"]["name"] + " " + data[i]["restaurant"]["location"]["locality"] + " || rating: " + data[i]["restaurant"]["user_rating"]["aggregate_rating"];

#content = page.text
#soup = BeautifulSoup(content, 'html.parser')


#print(soup.prettify())
