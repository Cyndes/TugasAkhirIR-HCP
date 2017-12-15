def integrate(query):
	# panggil search zomato
	#result_zomato = search_zomato(query)
	# panggil search openrice
	#result_openrice = search_openrice(query)
	# panggil search foody
	#result_foody = search_foody(query)
	# panggil search pergikuliner
	#result_pergikuliner = seach_pergi_kuliner(query)

	lovely_dummy_zomato = {'KFC - Pondok Indah': 
	   {'rating': 3.5, 
	    'review': 12, 
	    'address': "Pondok Indah Mall 2, Lt. 3, No. 14"
	   },
	 'McDonald - Jl. Margonda No. 23': 
	   {'rating': 4.6, 
	    'review': 24, 
	    'address': "Jl. Margonda No. 23, Beji, Depok"
	   },
	 'Pizza Hut - Jl. Margonda No. 7': 
	   {
	    'rating': 3.2, 
	    'review': 15, 
	    'address': "Jl. Margonda No.7, Depok"
	   }
	}

	lovely_dummy_openrice = {'KFC - Pondok Indah': 
	   {'rating': 7.6, 
	    'review': 7, 
	    'address': "Pondok Indah Mall 2, Lt. 3, No. 14"
	   },
	 'McDonald - Jl. Margonda No. 23': 
	   {'rating': 7.6, 
	    'review': 8, 
	    'address': "Jl. Margonda No. 23, Beji, Depok"
	   },
	 'Pizza Hut - Jl. Margonda No. 7': 
	   {
	    'rating': 7.6, 
	    'review': 9, 
	    'address': "Jl. Margonda No.7, Depok"
	   }
	}

	lovely_dummy_foody = {'KFC - Pondok Indah': 
	   {
	   	'foody_name': "KFC - Pondok Indah Mall 2",
	   	'rating': 7.6, 
	    'review': 11, 
	    'address': "Pondok Indah Mall 2, Lt. 3, No. 14"
	   },
	 'McDonald - Jl. Margonda No. 23': 
	   {
	   	'foody_name': "McDonald - Margonda",
	   	'rating': 7.6, 
	    'review': 12, 
	    'address': "Jl. Margonda No. 23, Beji, Depok"
	   },
	 'Pizza Hut - Jl. Margonda No. 7': 
	   {
	   	'foody_name': "Pizza Hut - Margonda",
	    'rating': 7.6, 
	    'review': 13, 
	    'address': "Jl. Margonda No.7, Depok"
	   }
	}

	lovely_dummy_pergikuliner = {'KFC - Pondok Indah': 
	   {'rating': 7.5, 
	    'review': 4, 
	    'address': "Pondok Indah Mall 2, Lt. 3, No. 14"
	   },
	 'McDonald - Jl. Margonda No. 23': 
	   {'rating': 5, 
	    'review': 5, 
	    'address': "Jl. Margonda No. 23, Beji, Depok"
	   },
	 'Pizza Hut - Jl. Margonda No. 7': 
	   {
	    'rating': 2.5, 
	    'review': 6, 
	    'address': "Jl. Margonda No.7, Depok"
	   },
	 'Pizza Hut - Jl. Lenteng Agung No. 2': 
	   {
	    'rating': 5, 
	    'review': 7, 
	    'address': "Jl. Lenteng Agung No.2, Jakarta Selatan"
	   }
	}

	#result = result_zomato
	result = lovely_dummy_zomato
	for key,value in lovely_dummy_openrice.items():
		if key in result.keys():
			result[key]['rating'] += value['rating']
			result[key]['review'] += value['review']
		else:
			result[key] = value

	for key,value in lovely_dummy_foody.items():
		if key in result.keys():
			result[key]['rating'] += value['rating']
			result[key]['review'] += value['review']
			result[key]['foody_name'] = value['foody_name']
		else:
			result[key] = value

	for key,value in lovely_dummy_pergikuliner.items():
		if key in result.keys():
			result[key]['rating'] += value['rating']
			result[key]['review'] += value['review']
		else:
			result[key] = value

	for key in result:
		result[key]['score'] = (0.4 * (result[key]['rating'] / 4.0)) + (0.6 * result[key]['review'])

	print result

restaurant = raw_input("Restaurants you want to find? ")
integrate(restaurant)