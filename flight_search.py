from datetime import datetime

# Search algorithm notes
# Ordered or unordered linear search ? 
#   benefits of ordered is that we can stop early during a search.
# Binary search algorithm ? 
# Ternary search algorithm ?

# Search flights
class FlightSearch:
    def __init__(self, flights):
        self.flights = flights

    # Currently not flexible
    def search(self, departure_city, arrival_city, date):
        date = datetime.strptime(date, "%Y-%m-%d")
        results = [
            flight for flight in self.flights
            if flight.departure_city == departure_city and
               flight.arrival_city == arrival_city and
               flight.date_time.date() == date.date() and
               flight.is_available()
        ]
        return results