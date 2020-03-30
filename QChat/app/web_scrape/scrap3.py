from bs4 import BeautifulSoup
import requests 
import json

src = requests.get('https://en.wikipedia.org/wiki/Misinformation_related_to_the_2019%E2%80%9320_coronavirus_pandemic#References').text
soup = BeautifulSoup(src, 'lxml')

references = soup.find('div', class_="mw-references-wrap mw-references-columns")
links = references.ol

URL=[]								# This is to store the URL's to the articles.

for webnews in soup.find_all('cite', class_="citation news"):
	link  = webnews.find('a')['href']
	# print(link)
	URL.append(link)
	# print()

for i in range(0,25):
	sources = requests.get(URL[i])					# Now we can search through ALL of these webpages! 
	
scrappy = BeautifulSoup(sources, 'lxml')


Misinformation=[]					# This is to store the actual paragraph's of info

for articles in scrappy.find_all('p'):
	info = articles.find('p').text
	print(info)
	Misinformation.append(info)		# This appends this into the URL
	print()

	with open("Wikipedia.json", "w") as write_file:
		json.dump(Misinformation, write_file)		


# This script will scrap information off of the Wikipedia page on Misinformation related to COVID-19
# and store the output as a JSON file 

# Hopefully we can then feed this data into the Neural Network!!! 
