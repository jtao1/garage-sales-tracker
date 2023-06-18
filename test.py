from Listing import Listing
from datetime import datetime, timedelta


location = '701 S Eola Rd, Aurora, IL 60504'
date_range = ['Fri Jun 9', 'Sun Jun 11']
coords = ['41.74317600', '-88.24923400']
times = '''
- Friday, June9, 2023 | 9:00 am - 4:00 pm
- Saturday, June 10, 2023 | 9:00 am - 5:30 pm
- Sunday, June 11, 2023 | 8:00 am - 2:30 pm
		'''
listing = Listing(location, date_range, times, coords)
with open('locations.txt', 'w') as file:
	file.write(str(datetime.utcnow()) + '\n')
	file.write(str(listing))
	file.write(str(listing.get_times())  + '\n')

with open('locations.txt', 'r') as file:
	line = file.readline().strip()
	print(line)
	dt = datetime.strptime(line, '%Y-%m-%d %H:%M:%S.%f')
	delta = (datetime.utcnow() - dt).total_seconds()
	print(delta)

coords = [ float(coord) for coord in listing.coords]
print(listing.coords)