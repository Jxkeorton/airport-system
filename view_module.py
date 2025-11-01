import pandas as pd
import csv
from data_structures import merge_sort

#hi

def load_csv_data(filename):
    """Reads a CSV file and returns a list of dictionaries."""
    with open(filename, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        return list(reader)


def view_flights_by_price():
    flights = load_csv_data("Flights.csv")

    # Convert CostPerSeat to float for sorting
    for f in flights:
        try:
            f["CostPerSeat"] = float(f["CostPerSeat"])
        except ValueError:
            f["CostPerSeat"] = 0.0  # handle missing or invalid data

    print("\nFlights Sorted by Cost (High → Low):")
    sorted_flights = merge_sort(flights, "CostPerSeat", reverse=True)

    for f in sorted_flights:
        print(
            f"{f['FlightID']} | {f['DepartureCity']} → {f['ArrivalCity']} "
            f"| €{f['CostPerSeat']} | {f['DateTime']} | {f['Status']}"
        )


def view_reservations_by_date():
    reservations = load_csv_data("Bookings.csv")

    if not reservations:
        print("No booking data found.")
        return

    print("\nBookings Sorted by Booking ID:")
    sorted_res = merge_sort(reservations, "BookingID")

    for r in sorted_res:
        print(
            f"{r['BookingID']} | Flight: {r['FlightID']} | Passenger: {r['PassengerID']} "
            f"| Seat: {r['SeatNumber']} | Status: {r['Status']}"
        )



def view_passengers():
    passengers = load_csv_data("Passengers.csv")

    if not passengers:
        print("No passenger data found.")
        return

    print("\nPassenger List:")
    for p in passengers:
        print(f"{p['PassengerID']} | {p['FirstName']} {p['Surname']} | DOB: {p['DOB']} | Email: {p['Email']}")

def view_main():
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


