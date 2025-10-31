import pandas as pd
from view_module import view_flights_by_price, view_passengers, view_reservations_by_date

def main_menu():
    while True:
        print("\n--- EDD Airlines Viewing System ---")
        print("1 - View Flights (by Price)")
        print("2 - View Reservations (by Date)")
        
        print("3 - View Passengers")
        print("0 - Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            view_flights_by_price()
        elif choice == "2":
            view_reservations_by_date()
        elif choice == "3":
            view_passengers()
        elif choice == "0":
            print("Exiting Viewer...")
            break
        else:
            print("Invalid choice. Try again!")


if __name__ == "__main__":
    main_menu()
