import os

from Flight_Manager_Panda import AirportDataOptimized
from flight_search import FlightSearch
from bookings import BookingSystem
from view_list import view_main

airport_data: AirportDataOptimized = AirportDataOptimized(
    flights_path="./data/Flights.csv",
    passengers_path="./data/Passengers.csv",
    bookings_path="./data/Bookings.csv",
    aircraft_path="./data/Aircraft.csv"
)

def clear_screen():
    # Windows
    if os.name == 'nt':
        os.system('cls')
    # macOS / Linux / Unix
    else:
        os.system('clear')

def main():
    while True:
        clear_screen()
        print("----------------------")
        print("  EDD Booking System  ")
        print("----------------------")
        print()
        print(" Select an Option:    ")
        print(" 1. Search a Flight   ")
        print(" 2. Book a Flight     ")
        print(" 3. View Flight Information")
        print(" 4. Admin Function    ")
        print(" 5. Exit")
        
        user_option = input("\nEnter your choice (1-5): ").strip()

        # --- OPTION 1: Search a Flight ---
        if user_option == "1":
            clear_screen()
            search = FlightSearch(airport_data)

            departure = input("Enter departure city: ")
            arrival = input("Enter arrival city: ")
            date = input("Enter date (YYYY-MM-DD): ")

            results = search.search(departure, arrival, date)
            if results:
                print("\nAvailable flights:")
                for flight in results:
                    print(flight)

                book_now = input("\nWould you like to book a seat? (yes/no): ").lower()
                if book_now == "yes":
                    clear_screen()
                    print("Loading Booking System...")
                    booking_system = BookingSystem(airport_data)
                    booking_system.interactive_booking()
                else:
                    input("\nPress Enter to return to the main menu...")
            else:
                print("\nNo flights available.")
                input("\nPress Enter to return to the main menu...")

        # --- OPTION 2: Book a Flight Directly ---
        elif user_option == "2":
            clear_screen()
            print("Loading Booking System...")
            booking_system = BookingSystem(
                flights_csv="./data/Flights.csv",
                passengers_csv="./data/Passengers.csv",
                bookings_csv="./data/Bookings.csv",
                aircraft_csv="./data/Aircraft.csv"
            )
            booking_system.interactive_booking()
            input("\nPress Enter to return to the main menu...")

        # --- OPTION 3: View a list of flights ---
        elif user_option == "3":
            view_main(               
                flights_csv="./data/Flights.csv",
                passengers_csv="./data/Passengers.csv",
                bookings_csv="./data/Bookings.csv"
            )

        # --- OPTION 4: Placeholder ---
        elif user_option == "4":
            print("\nFeature under development: Admin Function")
            input("\nPress Enter to return to the main menu...")

        # --- OPTION 5: Exit ---
        elif user_option == "5":
            clear_screen()
            print("Thank you for using the EDD Booking System. Goodbye!")
            break

        else:
            print("\nInvalid option. Please select 1-5.")
            input("\nPress Enter to try again...")

if __name__ == "__main__":
    main()
