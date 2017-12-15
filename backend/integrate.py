from scrappingzomato import *
from scrappingopenrice import *
from scrappingfoody import *
from scrappingpergikuliner import *

def integrate(query):
	# panggil search zomato
	#result_zomato = scrappingzomato.seach_restaurant(query)
	# panggil search openrice
	result_openrice = scrappingopenrice.seach_restaurant(query)
	# panggil search foody
	result_foody = scrappingfoody.seach_restaurant(query)
	# panggil search pergikuliner
	result_pergikuliner = scrappingpergikuliner.seach_restaurant(query)

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