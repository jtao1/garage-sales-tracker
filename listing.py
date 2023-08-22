def location_breakdown(location):
    breakdown = location.split(',')
    street = breakdown[0].strip()
    city = breakdown[1].strip()
    state_postal = breakdown[2].strip().split()
    state = state_postal[0]
    if (len(state_postal) == 2):
        postal = state_postal[1]
    else:
        postal = None
    return [street, city, state, postal]

class Listing:
    def __init__(self, location, date_range, times, coords): #str, list, str, list
        self.street, self.city, self.state, self.postal = location_breakdown(location)
        if len(date_range) == 2:
            self.date_start = date_range[0].strip()
            self.date_end = date_range[1].strip()
        else:
            self.date_start = date_range[0]
            self.date_end = date_range[0]
        self.times = times
        self.coords = coords
    
    def __str__(self):
        return f'{self.street}, {self.city}, {self.state} {self.postal} | {self.date_start} - {self.date_end} | {self.coords}'
    
    def get_times(self):
        return self.times

    def get_coords(self):
        return self.coords

    def get_data(self):
        return [f'{self.street}, {self.city}, {self.state}', self.postal, self.date_start, self.date_end, self.coords[0], self.coords[1]]

    def compare_to(self, other):
        # print('self', self.coords)
        # print('other', other.coords)
        if self.coords == other.coords:
            if self.date_start == other.date_start and self.date_end == other.date_end:
                return True
        return False

        # if self.street == other.street:
        #     if self.date_start == other.date_start and self.date_end == other.date_end:
        #         return True