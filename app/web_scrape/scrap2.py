from bs4 import BeautifulSoup
import requests 
import json

src = requests.get('https://en.wikipedia.org/wiki/Misinformation_related_to_the_2019%E2%80%9320_coronavirus_pandemic#References').text
soup = BeautifulSoup(src, 'lxml')

references = soup.find('div', class_="mw-references-wrap mw-references-columns")
links = references.ol

res=[[],[]]

for items in links.find_all('li'):
	text = items.text
	print(text)
	res[0].append(text)
	print()


print("###################  SOURCES  ##########################")

for webnews in soup.find_all('cite', class_="citation news"):
	link  = webnews.find('a')['href']
	print(link)
	res[1].append(link)
	print()

	with open("Misinformation.json", "w") as write_file:
		json.dump(res, write_file)




# This script will scrap information off of the Wikipedia page on Misinformation related to COVID-19
# and store the output as a JSON file 

# Hopefully we can then feed this data into the Neural Network!!! 
