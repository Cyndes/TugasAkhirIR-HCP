from scrapingzomato import *
from scrapingopenrice import *
from scrapingfoody import *
from scrapingpergikuliner import *

def integrate(query):
	# panggil search zomato
	#result_zomato = scrapingzomato.seach_restaurant(query)
	# panggil search openrice
	result_openrice = scrapingopenrice.seach_restaurant(query)
	# panggil search foody
	result_foody = scrapingfoody.seach_restaurant(query)
	# panggil search pergikuliner
	result_pergikuliner = scrapingpergikuliner.seach_restaurant(query)

	result = result_zomato
	for key,value in result_openrice.items():
		if key in result.keys():
			result[key]['no_of_occurences'] = 2
			result[key]['rating'] += value['rating']
			result[key]['review'] += value['review'] 
		else:
			result[key] = value
			result[key]['no_of_occurences'] = 1

	for key,value in result_foody.items():
		if key in result.keys():
			result[key]['no_of_occurences'] += 1
			result[key]['rating'] += value['rating']
			result[key]['review'] += value['review']
			result[key]['foody_name'] = value['foody_name']
		else:
			result[key] = value
			result[key]['no_of_occurences'] = 1

	for key,value in result_pergikuliner.items():
		if key in result.keys():
			result[key]['no_of_occurences'] += 1
			result[key]['rating'] += value['rating']
			result[key]['rating'] /= result[key]['no_of_occurences']
			result[key]['review'] += value['review']
		else:
			result[key] = value
			result[key]['no_of_occurences'] = 1

	for key in result:
		result[key]['score'] = (0.4 * result[key]['rating']) + (0.6 * result[key]['review'])

	print result

restaurant = raw_input("Restaurants you want to find? ")
integrate(restaurant)