from utils.sort_data import merge_sort

def view_flights_by_price(airport_data):
    flights = airport_data.flights.to_dict("records")  # Get flights as a list of dictionaries

    # Convert CostPerSeat to float for sorting
    for f in flights:
        try:
            f["CostPerSeat"] = float(f["CostPerSeat"])
        except ValueError:
            f["CostPerSeat"] = 0.0  # Handle missing or invalid data

    print("\nFlights Sorted by Cost (High → Low):")
    sorted_flights = merge_sort(flights, "CostPerSeat", reverse=True)

    for f in sorted_flights:
        print(
            f"{f['FlightID']} | {f['DepartureCity']} → {f['ArrivalCity']} "
            f"| €{f['CostPerSeat']} | {f['DateTime']} | {f['Status']}"
        )


def view_reservations_by_date(airport_data):
    reservations = airport_data.bookings.to_dict("records")  # Get bookings as a list of dictionaries

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


def view_passengers(airport_data):
    passengers = airport_data.passengers.to_dict("records")  # Get passengers as a list of dictionaries

    if not passengers:
        print("No passenger data found.")
        return

    print("\nPassenger List:")
    for p in passengers:
        print(f"{p['PassengerID']} | {p['FirstName']} {p['Surname']} | DOB: {p['DOB']} | Email: {p['Email']}")


def view_list(airport_data):
    while True:
        print("\n--- EDD Airlines Viewing System ---")
        print("1 - View Flights (by Price)")
        print("2 - View Reservations (by Date)")
        print("3 - View Passengers")
        print("0 - Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            view_flights_by_price(airport_data)
        elif choice == "2":
            view_reservations_by_date(airport_data)
        elif choice == "3":
            view_passengers(airport_data)
        elif choice == "0":
            print("Exiting Viewer...")
            break
        else:
            print("Invalid choice. Try again!")