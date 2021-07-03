
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
url = 'https://www.cancer.gov/about-cancer/treatment/drugs/breast'

#open connection
client = urlopen(url)
page_html = client.read()
#close connection
client.close()



page_soup = BeautifulSoup(page_html, "html.parser")

sections1 = page_soup.find("section", {"id": 1})
links1 = sections1.find_all('a')
drugs1 = [] #Drugs Approved to Prevent Breast Cancer
obj1 = {} 
for i in range(len(links1)):
	obj1["name"] = links1[i].text
	obj1["url"] = 'https://www.cancer.gov' + links1[i]['href']
	obj1_copy = obj1.copy()
	drugs1.append(obj1_copy)


sections2 = page_soup.find("section", {"id": 2})
links2 = sections2.find_all('a')
obj2 = {} 
drugs2 = [] #Drugs Approved to Treat Breast Cancer
for i in range(len(links2)):
	obj2["name"] = links2[i].text
	obj2["url"] = 'https://www.cancer.gov' + links2[i]['href']
	obj2_copy = obj2.copy()
	drugs2.append(obj2_copy)


sections3 = page_soup.find("section", {"id": 3})
links3 = sections3.find_all('a')
obj3 = {} 
drugs3 = [] #Drug Combinations Used in Breast Cancer
for i in range(len(links3)):
	obj3["name"] = links3[i].text
	obj3["url"] = 'https://www.cancer.gov' + links3[i]['href']
	obj3_copy = obj3.copy()
	drugs3.append(obj3_copy)
