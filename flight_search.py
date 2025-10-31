from datetime import datetime

# Search algorithm notes
# Ordered or unordered linear search ? 
#   benefits of ordered is that we can stop early during a search.
# Binary search algorithm ? 
#   if data cannot be sorted then you cannot use binary search.
# Ternary search algorithm ? 
#   Ternary search is a divide-and-conquer algorithm that works on sorted arrays.
#  It divides the array into three parts and determines which part may contain the target value.

# Create a data structure for each iteration of the search ? 
#   this could be achieved by sorting data as it is collected from the data structure in the file manager.
#   alternatively the data could be collected per key and then sorted into a list in the end through filtering and merging <- seems slower 

# TODO : 
#  connect to new flight manager.
#  Create new search algorithm with clever sorting and search using tips above
#  Make search more flexible

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