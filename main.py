import requests
import re
from bs4 import BeautifulSoup

def garagesalefinder_scraper():
	url = 'https://garagesalefinder.com/yard-sales/naperville-il/'
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	results = soup.find(id='city-sale-list')
	listings = results.find_all('div', class_='row collapse record')
	for listing in listings:
		address = listing.find('span', class_='sale-click').text.strip()
		date = listing.find('div', class_='sale-date').text.strip()
		print(f'{address} | {date}')
		print(listing, end='\n\n')

def gsalr_scraper():
	url = 'https://gsalr.com/garage-sales-naperville-il.html?loc=41.75082,-88.15292'
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	results = soup.find(id='listings')
	classes = ['listing upgrade l-data', 'listing l-data']
	for a_class in classes:
		listings = results.find_all('div', class_=a_class)
		for listing in listings:
			street = listing.find(attrs={'itemprop':'streetAddress'}).text.strip()
			locality = listing.find(attrs={'itemprop':'addressLocality'}).text.strip()
			region = listing.find(attrs={'itemprop':'addressRegion'}).text.strip()
			postal = listing.find(attrs={'itemprop':'postalCode'}).text.strip()
			start_date = listing.find(attrs={'itemprop':'startDate'}).attrs['content']
			end_date = listing.find(attrs={'itemprop':'endDate'}).attrs['content']
			print(f'{street}, {locality}, {region} {postal} | {start_date} - {end_date}')

url = 'https://yardsales.net/naperville-il/'
page = requests.get(url)
results = BeautifulSoup(page.content, 'html.parser')
listings = results.find_all(attrs={'itemprop':'url'})
for listing in listings:
	new_url = 'https://yardsales.net' + listing.attrs['href']
	page = requests.get(new_url)
	results = BeautifulSoup(page.content, 'html.parser')
	results = results.find(class_='sale-dates').text
	results = re.sub(r'[^\w\s,:-]', '|', results)[1:]
	results = results.split('|')
	location = results[-1][results[-1][:18].index('m',14)+1:]
	results[-1] = results[-1][:results[-1][:18].index('m',14)+1]
	print(location)
	for i in range(0, len(results), 2):
		print(f'{results[i].strip()} | {results[i+1].strip()}')
	

# with open('test.txt', 'w', encoding='unicode-escape') as f:
# 	f.write(results.prettify())
# 	f.close()




