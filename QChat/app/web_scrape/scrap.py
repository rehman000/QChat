from bs4 import BeautifulSoup
import requests 
import json

src = requests.get('https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports').text
soup = BeautifulSoup(src, 'lxml')

article = soup.find('div', id="PageContent_C006_Col01")
Situation_Report = article.div.div

res=[[],[]]

for report in Situation_Report.find_all('p'):
	text = report.text
	print(text)
	res[0].append(text)

	pdf = report.find('a')['href']
	pdf = pdf.split('/')[5]
	link =  f'https://www.who.int/docs/default-source/coronaviruse/situation-reports/{pdf}'
	print(link)
	res[1].append(link)

	print()

	with open("report.json", "w") as write_file:
		json.dump(res, write_file)
	


# This script will scrap information off of the world health organization on Situation reports related to COVID-19
# and store the output as a JSON file 

# Hopefully we can try to feed this data into the Neural Network!!! 
