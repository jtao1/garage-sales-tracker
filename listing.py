import scraper

def location_breakdown(location):
    breakdown = location.split(',')
    street = breakdown[0][:-1].trim()
    city = breakdown[1][:-1].trim()
    state_postal = breakdown[2].trim().split()
    state = state_postal[0]
    if (len(state_postal) == 2):
        postal = state_postal[1]
    else:
        postal = None
    return [street, city, state, postal]

class listing:
    def __init__(self, location, date_range, times):
        self.street, self.city, self.state, self.postal = location_breakdown(location)
        self.date_start = date_range[0]
        self.date_end = date_range[1]
        self.times = times

    def __str__(self):
        return f'{self.street}, {self.city}, {self.state} {self.postal} | {self.date_range}'
        

