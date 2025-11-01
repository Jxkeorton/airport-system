from utils.clear_screen import clear_screen
from Flight_Manager import AirportData
from flight_search import FlightSearch
from bookings import BookingSystem
from view_list import view_list

# Display a loading message
print("Loading Airport System... Please wait.")

# Initialize the airport data manager as a global instance
airport_data: AirportData = AirportData(
    flights_path="./data/Flights.csv",
    passengers_path="./data/Passengers.csv",
    bookings_path="./data/Bookings.csv",
    aircraft_path="./data/Aircraft.csv"
)

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
            search.flight_search()

        # --- OPTION 2: Book a Flight Directly ---
        elif user_option == "2":
            clear_screen()
            booking_system = BookingSystem(airport_data)
            booking_system.interactive_booking()
            input("\nPress Enter to return to the main menu...")

        # --- OPTION 3: View a list of flights ---
        elif user_option == "3":
            view_list(airport_data)

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
