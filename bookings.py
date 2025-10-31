import pandas as pd

from Flight_Manager_Panda import AirportDataOptimized

class BookingSystem:
    """Main booking system to handle flight seat reservations"""
    
    def __init__(self, flights_csv, passengers_csv, bookings_csv, aircraft_csv):
        # Use the optimized AirportDataOptimized class for data management
        self.data_manager = AirportDataOptimized(
            flights_path=flights_csv,
            passengers_path=passengers_csv,
            bookings_path=bookings_csv,
            aircraft_path=aircraft_csv
        )
        self.next_booking_id = self.get_next_booking_id()

    def get_next_booking_id(self):
        """Get the next available booking ID"""
        if self.data_manager.bookings.empty:
            return 1
        return int(self.data_manager.bookings['BookingID'].max()) + 1

    def seat_number_to_label(self, seat_number, seats_per_row):
        """Convert seat number to row + letter format (e.g., 1A, 12F)"""
        # Calculate row (1-indexed)
        row = ((seat_number - 1) // seats_per_row) + 1
        # Calculate position in row (0-indexed)
        seat_in_row = (seat_number - 1) % seats_per_row
        # Convert to letter (A, B, C, etc.)
        letter = chr(ord('A') + seat_in_row)
        return f"{row}{letter}"

    def seat_label_to_number(self, seat_label, seats_per_row):
        """Convert seat label (e.g., 1A, 12F) to seat number"""
        # Extract row number and letter
        row_str = ''.join(filter(str.isdigit, seat_label))
        letter = ''.join(filter(str.isalpha, seat_label)).upper()
        
        if not row_str or not letter:
            return None
        
        row = int(row_str)
        # Convert letter to position (A=0, B=1, etc.)
        seat_in_row = ord(letter) - ord('A')
        
        # Calculate seat number
        seat_number = (row - 1) * seats_per_row + seat_in_row + 1
        return seat_number

    def validate_passenger(self, passenger_id):
        """Check if passenger ID exists in the system using index"""
        passenger = self.data_manager.get_passenger_by_id(passenger_id)
        
        if passenger is None:
            return False, f"Error: Passenger ID {passenger_id} not found in the system."
        
        return True, f"Passenger validated: {passenger['FirstName']} {passenger['Surname']}"

    def validate_flight(self, flight_id):
        """Check if flight exists and is available for booking"""
        flight = self.data_manager.get_flight_by_id(flight_id)
        
        if flight is None:
            return False, f"Error: Flight ID {flight_id} not found."
        
        # Check if flight is scheduled or completed (not cancelled)
        if flight['Status'] == 'Cancelled':
            return False, f"Error: Flight {flight_id} has been cancelled."
        
        return True, f"Flight validated: {flight['DepartureCity']} to {flight['ArrivalCity']} on {flight['DateTime']}"

    def get_booked_seats(self, flight_id):
        """Get all currently booked seats for a flight (excluding cancelled bookings) using pandas"""
        # Use pandas filtering for efficient querying
        flight_bookings = self.data_manager.get_bookings_for_flight(flight_id)
        
        # Filter out cancelled bookings
        active_bookings = flight_bookings[flight_bookings['Status'] != 'Cancelled']
        
        # Return set of booked seat numbers
        return set(active_bookings['SeatNumber'].tolist())

    def get_available_seats(self, flight_id):
        """Get all available seats for a flight"""
        flight = self.data_manager.get_flight_by_id(flight_id)
        
        if flight is None:
            return None, None, f"Error: Flight {flight_id} not found."
        
        aeroplane_number = flight['AeroplaneNumber']
        
        # Get aircraft configuration using pandas index
        aircraft = self.data_manager.get_aircraft_by_id(aeroplane_number)
        
        if aircraft is None:
            return None, None, f"Error: Aircraft {aeroplane_number} configuration not found."
        
        # Get all possible seats based on aircraft configuration
        rows = int(aircraft['Rows'])
        seats_per_row = int(aircraft['SeatsInARow'])
        total_seats = rows * seats_per_row
        all_seats = set(range(1, total_seats + 1))
        
        # Get booked seats using pandas
        booked_seats = self.get_booked_seats(flight_id)
        
        # Calculate available seats
        available_seats = sorted(all_seats - booked_seats)
        
        # Check if flight is full
        if len(available_seats) == 0:
            return None, seats_per_row, f"Error: Flight {flight_id} is fully booked."
        
        return available_seats, seats_per_row, f"{len(available_seats)} seats available out of {total_seats} total seats."

    def display_available_seats(self, flight_id):
        """Display available seats in a formatted way with seat labels"""
        available_seats, seats_per_row, message = self.get_available_seats(flight_id)
        
        if available_seats is None:
            print(message)
            return None, None
        
        flight = self.data_manager.get_flight_by_id(flight_id)
        aeroplane_number = flight['AeroplaneNumber']
        aircraft = self.data_manager.get_aircraft_by_id(aeroplane_number)
        
        print(f"\n{message}")
        print(f"Aircraft: {aeroplane_number}")
        print(f"Configuration: {aircraft['Rows']} rows x {aircraft['SeatsInARow']} seats per row")
        
        # Convert seat numbers to labels
        seat_labels = [self.seat_number_to_label(seat, seats_per_row) for seat in available_seats]
        
        print("\nAvailable seats:")
        
        # Display seats in groups for readability
        for i in range(0, len(seat_labels), 10):
            print(", ".join(seat_labels[i:i+10]))
        
        return available_seats, seats_per_row

    def display_seat_map(self, flight_id):
        """Display a visual seat map showing available and booked seats"""
        available_seats, seats_per_row, message = self.get_available_seats(flight_id)
        
        if seats_per_row is None:
            print(message)
            return
        
        flight = self.data_manager.get_flight_by_id(flight_id)
        aircraft = self.data_manager.get_aircraft_by_id(flight['AeroplaneNumber'])
        rows = int(aircraft['Rows'])
        total_seats = rows * seats_per_row
        
        print(f"\n{'='*50}")
        print(f"SEAT MAP - Flight {flight_id}")
        print(f"{flight['DepartureCity']} → {flight['ArrivalCity']}")
        print(f"{'='*50}")
        
        # Create header with column letters
        header = "Row  " + "  ".join([chr(ord('A') + i) for i in range(seats_per_row)])
        print(f"\n{header}")
        print("-" * len(header))
        
        # Display each row
        for row in range(1, rows + 1):
            row_display = f"{row:3}  "
            for seat_pos in range(seats_per_row):
                seat_number = (row - 1) * seats_per_row + seat_pos + 1
                if seat_number in available_seats:
                    row_display += "◯  "  # Available seat
                else:
                    row_display += "●  "  # Booked seat
            print(row_display)
        
        print(f"\n◯ = Available  ● = Booked")
        print(f"{'='*50}\n")

    def book_seat(self, flight_id, passenger_id, seat_label):
        """Book a specific seat for a passenger on a flight using seat label (e.g., 1A, 12F)"""
        
        # Validate passenger
        valid, message = self.validate_passenger(passenger_id)
        if not valid:
            return False, message
        print(message)
        
        # Validate flight
        valid, message = self.validate_flight(flight_id)
        if not valid:
            return False, message
        print(message)
        
        # Get available seats
        available_seats, seats_per_row, message = self.get_available_seats(flight_id)
        if available_seats is None:
            return False, message
        
        # Convert seat label to seat number
        seat_number = self.seat_label_to_number(seat_label, seats_per_row)
        
        if seat_number is None:
            return False, f"Error: Invalid seat label '{seat_label}'. Please use format like 1A, 12F, etc."
        
        # Check if requested seat is available
        if seat_number not in available_seats:
            return False, f"Error: Seat {seat_label} is not available. Please choose from available seats."
        
        # Create new booking as a DataFrame row
        new_booking = pd.DataFrame([{
            'BookingID': self.next_booking_id,
            'FlightID': flight_id,
            'PassengerID': passenger_id,
            'SeatNumber': seat_number,
            'Status': 'Booked'
        }])
        
        # Append to bookings DataFrame using pandas concat
        self.data_manager.bookings = pd.concat(
            [self.data_manager.bookings, new_booking],
            ignore_index=True
        )
        
        # Update the booking index for fast lookups
        self.data_manager.booking_index[self.next_booking_id] = new_booking.to_dict('records')[0]
        
        self.next_booking_id += 1
        
        passenger = self.data_manager.get_passenger_by_id(passenger_id)
        flight = self.data_manager.get_flight_by_id(flight_id)
        
        success_message = f"""
Booking successful!
Booking ID: {new_booking['BookingID'].values[0]}
Passenger: {passenger['FirstName']} {passenger['Surname']}
Flight: {flight['DepartureCity']} to {flight['ArrivalCity']}
Date/Time: {flight['DateTime']}
Seat: {seat_label} (Seat Number: {seat_number})
Status: Booked
        """
        
        return True, success_message

    def save_bookings(self):
        """Save all bookings back to CSV file using pandas"""
        self.data_manager.save_data()
        return True, "✓ All data saved successfully."

    def interactive_booking(self):
        """Interactive booking process"""
        print("\n" + "="*50)
        print("FLIGHT SEAT BOOKING SYSTEM")
        print("="*50)
        
        try:
            # Get flight ID
            flight_id = int(input("\nEnter Flight ID: "))
            
            # Validate flight first
            valid, message = self.validate_flight(flight_id)
            if not valid:
                print(message)
                return
            
            # Display flight details
            flight = self.data_manager.get_flight_by_id(flight_id)
            print(f"\nFlight Details:")
            print(f"  Route: {flight['DepartureCity']} → {flight['ArrivalCity']}")
            print(f"  Date/Time: {flight['DateTime']}")
            print(f"  Aircraft: {flight['AeroplaneNumber']}")
            print(f"  Status: {flight['Status']}")
            
            # Get passenger ID
            passenger_id = int(input("\nEnter Your Passenger ID: "))
            
            # Ask if user wants to see seat map
            show_map = input("\nShow seat map? (yes/no): ").lower()
            if show_map == 'yes':
                self.display_seat_map(flight_id)
            else:
                # Display available seats as list
                available_seats, seats_per_row = self.display_available_seats(flight_id)
                if available_seats is None:
                    return
            
            # Get seat selection
            seat_label = input("\nEnter desired seat (e.g., 1A, 12F): ").upper()
            
            # Attempt booking
            success, message = self.book_seat(flight_id, passenger_id, seat_label)
            print(message)
            
            if success:
                # Ask if user wants to save
                save = input("\nSave booking to file? (yes/no): ").lower()
                if save == 'yes':
                    success, msg = self.save_bookings()
                    print(msg)

            
        except ValueError:
            print("Error: Please enter valid numeric values.")
        except Exception as e:
            print(f"Error: {e}")