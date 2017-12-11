from bs4 import BeautifulSoup

with open("foody.html") as fp:
	soup = BeautifulSoup(fp, 'html.parser')

print soup.head