from bs4 import BeautifulSoup
import requests 
import json

src = requests.get('https://en.wikipedia.org/wiki/Misinformation_related_to_the_2019%E2%80%9320_coronavirus_pandemic#References').text
soup = BeautifulSoup(src, 'lxml')

references = soup.find('div', class_="mw-references-wrap mw-references-columns")
links = references.ol

URL=[]

for webnews in soup.find_all('cite', class_="citation news"):
	link  = webnews.find('a')['href']
	print(link)
	URL.append(link)
	print()





# This script will scrap information off of the Wikipedia page on Misinformation related to COVID-19
# and store the output as a JSON file 

# Hopefully we can then feed this data into the Neural Network!!! 
