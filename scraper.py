import requests
import re
from Listing import *
from bs4 import BeautifulSoup


def save_locations(locations):
	with open('locations.txt', 'w') as file:
		for location in locations:
			print(location)
			file.write(location + '\n')
	file.close()

def update_locations(city, locations, new_listing):
	if city in locations:
		locations[city].append(new_listing)
	else:
		locations[city] = [new_listing]
	return locations


def garagesalefinder_scraper():
	locations = {}
	url = 'https://garagesalefinder.com/yard-sales/naperville-il/'
	main_page = requests.get(url)
	soup = BeautifulSoup(main_page.content, 'html.parser')
	results = soup.find(id='city-sale-list')
	classes = ['row collapse record upgraded', 'row collapse record']
	for a_class in classes:
		listings = results.find_all('div', class_=a_class)
		for listing in listings:
			address_zip = listing.find('span', class_='sale-click').text.strip()
			# zip_code = address_zip.split()[-1].strip()
			city = address_zip.split(',')[1].strip()
			# address = address_zip[0:address_zip.index(zip_code)].strip()
			date_range = listing.find('div', class_='sale-date').text.strip()
			date_range = re.sub(r',', '', date_range)
			date_range = re.split(r'[^\w\s]', date_range)
			link = listing.find(class_='sale-url').attrs['href']
			page = requests.get(link)
			result = BeautifulSoup(page.content, 'html.parser')
			times = result.find_all(class_='date-time')
			sale_times = ''
			for time in times:
				time = time.text.strip()
				days = time[:time.index(',',10)+6]
				hours = time[time.index(',',10)+6:]
				sale_times += f'{days} | {hours}\n'
				#print(f'{days} | {hours}')
			new_listing = Listing(address_zip, date_range, sale_times)
			print(new_listing)
			new_listing.get_times()
			locations = update_locations(city, locations, new_listing)

def gsalr_scraper():
	locations = {}
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

def yardsalesnet_scraper():
	locations = {}
	cur_listing = -1
	total_listings = 0
	page_num = 1
	while (cur_listing <= total_listings):
		url = f'https://yardsales.net/naperville-il/p:{page_num}'
		page = requests.get(url)
		results = BeautifulSoup(page.content, 'html.parser')
		if (page_num == 1):
			listing_count = results.find_all(class_='page-nav-count')[-1].text
			total_listings = listing_count[(listing_count.index('of') + 2):].strip()
			cur_listing = listing_count[(listing_count.index('-') + 2):(listing_count.index('of'))].strip()
		listings = results.find_all(attrs={'itemprop':'url'})		
		for listing in listings:
			new_url = 'https://yardsales.net' + listing.attrs['href']
			page = requests.get(new_url)
			results = BeautifulSoup(page.content, 'html.parser')
			results = results.find(class_='sale-dates').text
			results = re.sub(r'[^\w\s&\-,:.]', '|', results)[1:]
			results = results.split('|')
			print(results)
			address = results[-1][results[-1][:18].index('m', 14)+1:]
			print(address)
			# locations.append(address)
			results[-1] = results[-1][:results[-1][:18].index('m', 14)+1]
			# for i in range(0, len(results), 2):
			# 	print(f'{results[i].strip()} | {results[i+1].strip()}')
		if (cur_listing <= total_listings):
			page_num += 1

def main():
	garagesalefinder_scraper()
	# gsalr_scraper()
	# yardsalesnet_scraper()
	# locations = [*set(locations)]
	# save_locations(locations)

main()
