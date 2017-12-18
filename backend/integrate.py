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
			result[key]['foody_name'] = value['foody_name']
		else:
			result[key] = value
			result[key]['no_of_occurences'] = 1

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


def details(name, foody_name):
	# panggil search zomato
	details_zomato = see_details_zomato(name)
	# panggil search foody
	details_foody = see_details_foody(foody_name)
	# panggil search pergikuliner
	details_pergikuliner = see_details_pergikuliner(name)
	# panggil search openrice
	# details_openrice = see_details_openrice(name)

	print "details_zomato"
	print details_zomato
	print
	print "details_openrice"
	# print details_openrice
	print
	print "details_foody"
	print details_foody
	print
	print "details_pergikuliner"
	print details_pergikuliner
# query = raw_input("Restaurants you want to find? ")
# # integrate(query)
restaurant = {"name" : "Sushi Tei - Central Park", "foody_name" : "Sushi Tei - Central Park", "alamat" : "Jl. Lenteng Agung, No. 23"}
details(restaurant["name"], restaurant["foody_name"])