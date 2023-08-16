import requests
import re
from datetime import datetime
from listing import *
from bs4 import BeautifulSoup


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
			try:
				address_zip = listing.find('span', class_='sale-click').text.strip()
				# zip_code = address_zip.split()[-1].strip()
				city = address_zip.split(',')[1].strip()
				# address = address_zip[0:address_zip.index(zip_code)].strip()
				date_range = listing.find('div', class_='sale-date').text.strip()
				date_range = re.sub(r',', '', date_range)
				date_range = re.sub(r'  ', ' ', date_range)
				date_range = re.split(r'[^\w\s]', date_range)
				coord_lat = listing.attrs['data-sale'].split(',')[2].split(':')[1].strip()
				coord_lon = listing.attrs['data-sale'].split(',')[3].split(':')[1].strip()
				coords = [coord_lat, coord_lon]
				link = listing.find(class_='sale-url').attrs['href']
				page = requests.get(link)
				result = BeautifulSoup(page.content, 'html.parser')
				times = result.find_all(class_='date-time')
				sale_times = ''
				for time in times:
					time = time.text.strip()
					days = time[:time.index(',',10)+6]
					days = re.sub('  ', ' ', days)
					hours = time[time.index(',',10)+6:]
					sale_times += f'- {days} | {hours}\n'
					#print(f'{days} | {hours}')
				new_listing = Listing(address_zip, date_range, sale_times, coords)
				# print(new_listing)
				# print(new_listing.get_times())
				locations = update_locations(city, locations, new_listing)
			except Exception as e:
				print(e)
				pass
	return locations

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
			try:
				coord_lat = listing.attrs['data-lat']
				coord_lon = listing.attrs['data-lon']
				coords = [coord_lat, coord_lon]
				street = listing.find(attrs={'itemprop':'streetAddress'}).text.strip()
				city = listing.find(attrs={'itemprop':'addressLocality'}).text.strip()
				state = listing.find(attrs={'itemprop':'addressRegion'}).text.strip()
				postal = listing.find(attrs={'itemprop':'postalCode'}).text.strip()
				# start_date = listing.find(attrs={'itemprop':'startDate'}).attrs['content']
				# end_date = listing.find(attrs={'itemprop':'endDate'}).attrs['content']
				listing_url = listing.find(class_='sale-title').attrs['href']
				page = requests.get(listing_url)
				result = BeautifulSoup(page.content, 'html.parser')
				times = result.find_all(class_='date-time')
				if len(times) == 0:
					sale_times = ''
					date_range = ['', '']
				else:
					start_date = re.sub(r'[^\w\s&\-,:.]', '', times[0].text.strip())
					start_date = start_date.split(',')
					start_date = f'{start_date[0]}{start_date[1]}'
					end_date = re.sub(r'[^\w\s&\-,:.]', '', times[-1].text.strip())
					end_date = end_date.split(',')
					end_date = f'{end_date[0]}{end_date[1]}'
					date_range = [start_date, end_date]
					# print(date_range)
					address = f'{street}, {city}, {state} {postal}'
					sale_times = ''
					date_mapping = {'Mon': 'Monday', 'Tue': 'Tuesday', 'Wed': 'Wednesday', 'Thu': 'Thursday',
									'Fri': 'Friday', 'Sat': 'Saturday', 'Sun': 'Sunday'}
					for time in times:
						time = re.sub(r'[^\w\s&\-,:.]', '', time.text.strip())
						time = re.sub(r'^[aA-zZ]{3}', lambda x: date_mapping[x.group()], time)
						time = re.sub(r'([\d]{4})', lambda x: f'{x.group()} |', time)
						sale_times += f'- {time} \n'
				new_listing = Listing(address, date_range, sale_times, coords)
				# new_listing.get_coords()
				locations = update_locations(city, locations, new_listing)
			except Exception as e:
				print(e)
				pass
	return locations

def yardsalesnet_scraper():
	locations = {}
	cur_listing = -1
	total_listings = 0
	page_num = 0
	while (cur_listing < total_listings):
		# print('page: ', page_num)
		url = f'https://yardsales.net/naperville-il/p:{page_num}/'
		page = requests.get(url)
		results = BeautifulSoup(page.content, 'html.parser')
		listing_count = results.find_all(class_='page-nav-count')[-1].text
		total_listings = int(listing_count[(listing_count.index('of') + 2):].strip())
		cur_listing = int(listing_count[(listing_count.index('-') + 2):(listing_count.index('of'))].strip())
		listings = results.find_all(attrs={'itemtype':'http://schema.org/Event'})
		# print(listings)
		for listing in listings:
			try:
				date_range = listing.find(class_='dates').text.strip()
				date_range = re.sub(',', '', date_range).split('-')
				coords = listing.attrs['data-coords'].split(',')
				new_url = 'https://yardsales.net' + listing.find(attrs={'itemprop':'url'}).attrs['href']
				page = requests.get(new_url)
				results = BeautifulSoup(page.content, 'html.parser')
				address = results.find(class_='map-address').text.strip()
				results = results.find(class_='sale-dates').text
				results = re.sub(r'[^\w\s&\\\-,:./]', '|', results)[1:]
				if results.find(':') == -1:
					sale_times = ''
				else:
					results = results.split('|')
					results[-1] = results[-1][:results[-1][:18].index('m', 14)+1]
					sale_times = ''
					for i in range(0, len(results), 2):
						# print(f'{results[i].strip()} | {results[i+1].strip()}')
						sale_times += f'- {results[i].strip()} | {results[i+1].strip()}\n'
				city = address.split(',')[1].strip()
				new_listing = Listing(address, date_range, sale_times, coords)
				locations = update_locations(city, locations, new_listing)
			except Exception as e:
				print(e)
				pass
			# print(new_listing.get_coords())
		if (cur_listing < total_listings):
			page_num += 1
			# print('page: ', page_num, 'cur listing: ', cur_listing)
	# print(locations)
	return locations 

def merge_dicts(dict1, dict2):
	cities = list(set([*dict1.keys()] + [*dict2.keys()]))
	#print(cities)
	for city in cities:
		# print('city: ', city)
		try:
			locations_2 = dict2[city]
			#print(locations_2)
		except:
			continue
		try:
			locations_1 = dict1[city]
			#print(locations_1)
			for location_2 in locations_2:
				# print('loc2: ', location_2)
				for location_1 in locations_1:
					temp = []
					# print('loc1: ', locations_1)
					if location_1.compare_to(location_2) == False:
						temp.append(location_2)
				locations_1 += temp
		except KeyError:
			dict1[city] = dict2[city]
	return dict1
	
def save_locations(locations):
	num_listing = 0
	with open('locations.txt', 'w') as file:
		file.write(str(datetime.utcnow()) + '\n')
		for city in locations:
			listings = locations[city]
			for listing in listings:
				num_listing += 1
				file.write(str(listing) + '\n')
				file.write(str(listing.get_times())  + '\n')

		final = f'The total number of listings is: {num_listing}'
		file.write(final + '\n')

def write_file():
	with open('locations.txt', 'r') as file:
		file_time = datetime.strptime(file.readline().strip(), '%Y-%m-%d %H:%M:%S.%f')
		delta = (datetime.utcnow() - file_time).total_seconds()		
	if delta >= 82800: #23 hours = 82800 seconds
		with open('locations.txt', 'w') as file:
			garagesalefinder = garagesalefinder_scraper()
			print('len: ', len(garagesalefinder))
			gsalr = gsalr_scraper()
			print('len: ', len(gsalr))
			merged =  merge_dicts(garagesalefinder, gsalr)
			print('len: ', len(merged))
			yardsalesnet = yardsalesnet_scraper()
			print('len: ', len(yardsalesnet))
			merged = merge_dicts(merged, yardsalesnet)
			print('len: ', len(merged))
			save_locations(merged)	

def read_file():
	with open('locations.txt', 'r') as file:
		listings = []
		file_time = datetime.strptime(file.readline().strip(), '%Y-%m-%d %H:%M:%S.%f')
		lines = file.readlines()
		sale_times = ''
		location = ''
		date_range = ''
		coords = ''
		for line in lines:
				if line == '\n':
					date_range = date_range.split('-')
					new_listing = Listing(location, date_range, sale_times, coords)
					listings.append(new_listing)
					sale_times = ''
				else:
					if line[0] == '-':
						sale_times += line
					else:
						if line.find('The total number of listings') == -1:
							# print(line.split('|'))
							[location, date_range, coords] = line.split('|')
							coords = coords.split(',')
							lat = coords[0][coords[0].index("'")+1:-1]
							lon = coords[1][coords[1].index("'")+1:-3]
							coords = (lat, lon)
		return listings

def main():
	write_file()
	print('pass')
	listings = read_file()
	# for listing in listings:
	# 	print(listing)


# main()