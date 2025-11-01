# Search algorithm notes
# Ordered or unordered linear search ? 
#   benefits of ordered is that we can stop early during a search.
# Binary search algorithm ? 
#   if data cannot be sorted then you cannot use binary search.
# Ternary search algorithm ? 
#   Ternary search is a divide-and-conquer algorithm that works on sorted arrays.
#  It divides the array into three parts and determines which part may contain the target value.
# Interpolation search ? 
#   Interpolation search is an improved variant of binary search that works on the probing position of
#   the required value. It is best suited for uniformly distributed data. 
#   could use this method to search via date ranges if data is sorted by date.

# consider search algorithms specific to numeric and non numeric data ?

# Justify programming language used 

# Create a data structure for each iteration of the search ? 
#   this could be achieved by sorting data as it is collected from the data structure in the file manager.
#   alternatively the data could be collected per key and then sorted into a list in the end through filtering and merging <- seems slower 

# TODO : 
#  connect to new flight manager.
#  Create new search algorithm with clever sorting and search using tips above
#  Make search more flexible

# Search flights

from Flight_Manager import AirportDataOptimized
from bookings import BookingSystem
from utils.clear_screen import clear_screen

from datetime import datetime
import pandas as pd

class FlightSearch:
    def __init__(self, airport_data: AirportDataOptimized):
        self.airport_data = airport_data

    def search(self, departure_city, arrival_city, date):
        """
        Search for flights based on departure city, arrival city, and date.
        """
        # Convert the date string to a datetime object
        date = datetime.strptime(date, "%Y-%m-%d").date()

        # Use Pandas DataFrame filtering for efficient searching
        flights_df = self.airport_data.flights
        results = flights_df[
            (flights_df['DepartureCity'] == departure_city) &
            (flights_df['ArrivalCity'] == arrival_city) &
            (pd.to_datetime(flights_df['DateTime']).dt.date == date) &
            (flights_df['Status'] == "Scheduled")
        ]

        # Convert the filtered DataFrame to a list of dictionaries (or another format if needed)
        return results.to_dict('records')

    def interactive_search_and_booking(self):
        """
        Perform an interactive flight search and handle booking logic.
        """
        departure = input("Enter departure city: ")
        arrival = input("Enter arrival city: ")
        date = input("Enter date (YYYY-MM-DD): ")

        results = self.search(departure, arrival, date)
        if results:
            print("\nAvailable flights:")
            for flight in results:
                print(flight)

            book_now = input("\nWould you like to book a seat? (yes/no): ").lower()
            if book_now == "yes":
                clear_screen()
                print("Loading Booking System...")
                booking_system = BookingSystem(self.airport_data)
                booking_system.interactive_booking()
            else:
                input("\nPress Enter to return to the main menu...")
        else:
            print("\nNo flights available.")
            input("\nPress Enter to return to the main menu...")