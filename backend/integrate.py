from scrapingzomato import search_zomato
from scrapingopenrice import search_openrice
from scrapingfoody import search_foody
from scrapingpergikuliner import search_pergikuliner

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
			result[key]['review'] += int(value['review'])
		else:
			result[key] = value
			result[key]['no_of_occurences'] = 1

	for key in result:
		result[key]['score'] = round((0.4 * result[key]['rating']) + (0.6 * int(result[key]['review'])), 2)
		result[key]['score'] = round(result[key]['score'] * (result[key]['no_of_occurences'] / 4.0), 2)

	print result

restaurant = raw_input("Restaurants you want to find? ")
integrate(restaurant)