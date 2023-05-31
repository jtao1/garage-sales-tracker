import requests
import re
from bs4 import BeautifulSoup


def save_locations(locations):
	print('hi')
	with open('locations.txt', 'w') as file:
		for location in locations:
			print(location)
			file.write(location + '\n')
	file.close()

def garagesalefinder_scraper(locations):
	url = 'https://garagesalefinder.com/yard-sales/naperville-il/'
	main_page = requests.get(url)
	soup = BeautifulSoup(main_page.content, 'html.parser')
	results = soup.find(id='city-sale-list')
	classes = ['row collapse record upgraded', 'row collapse record']
	for a_class in classes:
		listings = results.find_all('div', class_=a_class)
		for listing in listings:
			address_zip = listing.find('span', class_='sale-click').text.strip()
			address = address_zip(address_zip[0:len(address_zip) - 5])
			locations.append(address[0:len(address) - 5])
			print(address[0:len(address) - 5])
			date = listing.find('div', class_='sale-date').text.strip()
			link = listing.find(class_='sale-url').attrs['href']
			page = requests.get(link)
			result = BeautifulSoup(page.content, 'html.parser')
			times = result.find_all(class_='date-time')
			print(f'{address} | {date}')
			# for time in times:
			# 	time = time.text.strip()
			# 	hours = time[time.index(',',10)+6:]
			# 	days = time[:time.index(',',10)+6]
			# 	print(f'{days} | {hours}')
			# print()

def gsalr_scraper(locations):
	url = 'https://gsalr.com/garage-sales-naperville-il.html?loc=41.75082,-88.15292'
	main_page = requests.get(url)
	soup = BeautifulSoup(main_page.content, 'html.parser')
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
			listing_url = listing.find(class_='sale-title').attrs['href']
			page = requests.get(listing_url)
			result = BeautifulSoup(page.content, 'html.parser')
			times = result.find_all(class_='date-time')
			locations.append(f'{street}, {locality}, {region}')
			# print(f'{street}, {locality}, {region} {postal} | {start_date} - {end_date}')
			# for time in times:
			# 	time = re.sub(r'[^\w\s&\-,:.]', '', time.text.strip())
			# 	print(time)
			# print()

def yardsalesnet_scraper(locations):
	locations = {}
	url = 'https://yardsales.net/naperville-il/'
	page = requests.get(url)
	results = BeautifulSoup(page.content, 'html.parser')
	listings = results.find_all(attrs={'itemprop':'url'})
	for listing in listings:
		new_url = 'https://yardsales.net' + listing.attrs['href']
		page = requests.get(new_url)
		results = BeautifulSoup(page.content, 'html.parser')
		results = results.find(class_='sale-dates').text
		results = re.sub(r'[^\w\s&\-,:.]', '|', results)[1:]
		results = results.split('|')
		# print(results)
		address = results[-1][results[-1][:18].index('m', 14)+1:]
		# print(address)
		locations.append(address)
		results[-1] = results[-1][:results[-1][:18].index('m', 14)+1]
		# for i in range(0, len(results), 2):
		# 	print(f'{results[i].strip()} | {results[i+1].strip()}')

def unique_listings():
	locations = {}

def main():
	locations = []
	# garagesalefinder_scraper(locations)
	# gsalr_scraper(locations)
	# yardsalesnet_scraper(locations)
	# locations = [*set(locations)]
	# save_locations(locations)

main()

