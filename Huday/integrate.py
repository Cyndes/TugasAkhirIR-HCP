# Isi dari result foody kurang lebih kaya gini:
#{
#"Nama - Alamat Sampe Sebelum Koma" : 
#	{
#	"foody_name" : "Nama di Foody"
#	"rating" : 7.6, 
#	"review" : 24,
#	"alamat" : "alamat lengkap"
#	}
#}

def integrate(query):
	# panggil search zomato
	result_zomato = search_zomato(query)
	# panggil search openrice
	result_openrice = search_openrice(query)
	# panggil search foody
	result_foody = search_foody(query)
	# panggil search pergikuliner
	result_pergikuliner = seach_pergi_kuliner(query)
	
	