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

        # Convert DateTime column to datetime objects
        self.airport_data.flights['DateTime'] = pd.to_datetime(self.airport_data.flights['DateTime'])

        # Create a new column for the date only (ignoring time)
        self.airport_data.flights['Date'] = self.airport_data.flights['DateTime'].dt.date

        # Sort and index the DataFrame by DepartureCity, ArrivalCity, and Date
        self.airport_data.flights.sort_values(by=['DepartureCity', 'ArrivalCity', 'Date'], inplace=True)
        self.airport_data.flights.set_index(['DepartureCity', 'ArrivalCity', 'Date'], inplace=True)

    def search(self, departure_city, arrival_city, date):
        """
        Search for flights based on departure city, arrival city, and date.
        """
        try:
            # Convert the input date to a datetime.date object
            date = datetime.strptime(date, "%Y-%m-%d").date()

            # Use the index to filter data
            results = self.airport_data.flights.loc[(departure_city, arrival_city, date)]

            # Ensure the result is always a DataFrame
            if isinstance(results, pd.Series):
                results = pd.DataFrame([results])

            # Convert the filtered DataFrame to a list of dictionaries
            return results.reset_index().to_dict('records')
        except KeyError:
            # No matching flights found
            return []

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
                print(f"\n ---- Flight Details ----")
                print(f"  Route: {flight['DepartureCity']} → {flight['ArrivalCity']}")
                print(f"  Date/Time: {flight['DateTime']}")
                print(f"  Aircraft: {flight['AeroplaneNumber']}")
                print(f"  Filght ID: {flight['FlightID']}")
                print(f"  -----------------------")


            book_now = input("\nWould you like to book a seat? (yes/no): ").lower()
            if book_now == "yes":
                booking_system = BookingSystem(self.airport_data)
                booking_system.interactive_booking()
            else:
                input("\nPress Enter to return to the main menu...")
        else:
            print("\nNo flights available.")
            input("\nPress Enter to return to the main menu...")