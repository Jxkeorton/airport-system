# TODO : 
#  Make search more flexible

from Flight_Manager import AirportData
from bookings import BookingSystem
from utils.clear_screen import clear_screen

from datetime import datetime
import pandas as pd

class FlightSearch:
    def __init__(self, airport_data: AirportData):
        self.airport_data = airport_data
        # Sort and index the DataFrame during initialization
        self.airport_data.flights.sort_values(by=['DepartureCity', 'ArrivalCity', 'DateTime'], inplace=True)
        self.airport_data.flights.set_index(['DepartureCity', 'ArrivalCity', 'DateTime'], inplace=True)

    def search(self, departure_city, arrival_city, date):
        """
        Search for flights based on departure city, arrival city, and date.
        """
        # Convert the date string to a datetime object
        date = datetime.strptime(date, "%Y-%m-%d")

        # Use the index to filter data
        try:
            results = self.airport_data.flights.loc[(departure_city, arrival_city, date)]
        except KeyError:
            # No matching flights found
            return []

        # Convert the filtered DataFrame to a list of dictionaries
        return results.to_dict('records')

    def flight_search(self):
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
                booking_system = BookingSystem(self.airport_data)
                booking_system.interactive_booking()
            else:
                input("\nPress Enter to return to the main menu...")
        else:
            print("\nNo flights available.")
            input("\nPress Enter to return to the main menu...")