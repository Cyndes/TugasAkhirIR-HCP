from scrapingzomato import search_zomato
from scrapingopenrice import search_openrice
from scrapingfoody import search_foody
from scrapingpergikuliner import search_pergikuliner
from scrapingzomato import see_details_zomato
from scrapingopenrice import see_details_openrice
from scrapingfoody import see_details_foody
from scrapingpergikuliner import see_details_pergikuliner
from collections import OrderedDict

def integrate(query):
	# panggil search zomato
	result_zomato = search_zomato(query)
	# panggil search openrice
	result_openrice = search_openrice(query)
	# panggil search foody
	result_foody = search_foody(query)
	print result_foody
	# panggil search pergikuliner
	result_pergikuliner = search_pergikuliner(query)
	
	result = {}
	for key,value in result_zomato.items():
		result[key] = value
		result[key]['no_of_occurences'] = 1

	for key,value in result_openrice.items():
		if key in result.keys():
			result[key]['no_of_occurences'] += 1
			result[key]['rating'] += value['rating']
			result[key]['review'] += int(value['review']) 
		else:
			result[key] = value
			result[key]['no_of_occurences'] = 1

	for key,value in result_foody.items():
		if key in result.keys():
			result[key]['no_of_occurences'] += 1
			result[key]['rating'] += value['rating']
			result[key]['review'] += int(value['review'])
			# result[key]['foody_name'] = value['foody_name']
			result[key]['url'] = "/details?name=" + key + "&addr=" + result[key]['alamat'].split(",")[0] + "&fd="
		else:
			result[key] = value
			result[key]['no_of_occurences'] = 1
			result[key]['url'] = "/details?name=" + key + "&addr=" + result[key]['alamat'].split(",")[0] + "&fd="

	for key,value in result_pergikuliner.items():
		if key in result.keys():
			result[key]['no_of_occurences'] += 1
			result[key]['rating'] += value['rating']
			result[key]['rating'] /= result[key]['no_of_occurences']
			result[key]['rating'] = round(result[key]['rating'], 2)
			result[key]['review'] += int(value['review'])
		else:
			result[key] = value
			result[key]['no_of_occurences'] = 1

	for key in result:
		result[key]['score'] = round((0.4 * result[key]['rating']) + (0.6 * int(result[key]['review'])), 2)
		result[key]['score'] = round(result[key]['score'] * (result[key]['no_of_occurences'] / 4.0), 2)

	od = OrderedDict(sorted(result.items(), key=lambda x: x[1]['score'], reverse=True))
	return od


def integrate_details(name, foody_name, address):
	# panggil search zomato
	details_zomato = see_details_zomato(name)
	# panggil search foody
	# details_foody = see_details_foody(foody_name)
	# panggil search pergikuliner
	details_pergikuliner = see_details_pergikuliner(name, address)
	# panggil search openrice
	details_openrice = see_details_openrice(name)

	result = {}
	result["name"] = details_zomato["name"]
	result["telephone"] = details_pergikuliner["telephone"]
	result["address"] = details_zomato["address"]
	result["rating_zomato"] = details_zomato["rating"]
	# result["rating_foody"] = details_foody["rating"]
	result["rating_pergikuliner"] = details_pergikuliner["rating"]
	result["rating_openrice"] = details_openrice["rating"]
	result["review_zomato"] = details_zomato["review"]
	# result["review_foody"] = details_foody["review"]
	result["review_openrice"] = details_openrice["review"]
	result["cuisine"] = details_zomato["cuisine"]
	result["payment"] = details_pergikuliner["payment"]
	result["opening_hours"] = details_pergikuliner["opening_hours"]
	result["avg_cost"] = details_zomato["avg_cost"]
	result["facilities"] = details_pergikuliner["facilities"]
	result["recommended_menu"] = details_openrice["recommended_menu"]
	result["capacity"] = details_openrice["capacity"]

	return result

	# print "details_zomato"
	# print details_zomato
	# print
	# print "details_openrice"
	# print details_openrice
	# print
	# print "details_foody"
	# print details_foody
	# print
	# print "details_pergikuliner"
	# print details_pergikuliner
# query = raw_input("Restaurants you want to find? ")
# # integrate(query)
# restaurant = {"name" : "Sushi Tei - Central Park", "foody_name" : "Sushi Tei - Central Park", "alamat" : "Jl. Lenteng Agung, No. 23"}
# details(restaurant["name"], restaurant["foody_name"])