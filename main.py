# Searching for available flights between two cities on a given date. 
# (Flight ID, Departure City, Arrival City, Date & Time,  Flight Available - True/False)
# If the list is sorted we can use binary search for the date and time

# Ideas for global objects:
#  - flight manager
#  - The flight itself 

from flight_manager import FlightManager
from flight_search import FlightSearch

def main():
    manager = FlightManager("mockData.csv")
    search = FlightSearch(manager.flights)

    departure = input("Enter departure city: ")
    arrival = input("Enter arrival city: ")
    date = input("Enter date (YYYY-MM-DD): ")

    results = search.search(departure, arrival, date)
    if results:
        print("Available flights:")
        for flight in results:
            print(flight)
    else:
        print("No flights available.")

if __name__ == "__main__":
    main()