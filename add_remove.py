# -*- coding: utf-8 -*-
"""
Flight Management System - Integrated with AirportData
Handles adding, cancelling, and deleting flights, bookings, passengers, and aircraft
"""

import pandas as pd
from Flight_Manager import AirportData
from datetime import datetime


class AdminManager:
    """Admin management system for adding/removing flights, passengers, bookings, and aircraft"""
    
    def __init__(self, airport_data: AirportData):
        self.data_manager = airport_data
    
    # ==================== VALIDATION METHODS ====================
    
    def validate_date(self, date_str, date_format="%Y-%m-%d"):
        """Validate date format and ensure it's a valid date"""
        try:
            date_obj = datetime.strptime(date_str, date_format)
            return True, date_obj
        except ValueError:
            return False, None
    
    def validate_datetime(self, datetime_str, datetime_format="%Y-%m-%d %H:%M:%S"):
        """Validate datetime format and ensure it's valid"""
        try:
            datetime_obj = datetime.strptime(datetime_str, datetime_format)
            # Check if the datetime is in the past
            if datetime_obj < datetime.now():
                return False, None, "DateTime cannot be in the past"
            return True, datetime_obj, None
        except ValueError:
            return False, None, "Invalid date/time format. Use YYYY-MM-DD HH:MM:SS"
    
    def validate_email(self, email):
        """Basic email validation"""
        if '@' not in email or '.' not in email:
            return False, "Invalid email format"
        return True, None
    
    def validate_phone(self, phone):
        """Basic phone number validation"""
        # Remove common separators
        clean_phone = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
        if not clean_phone.isdigit() or len(clean_phone) < 7:
            return False, "Invalid phone number format"
        return True, None

    def get_dataframe(self, category):
        """Get the appropriate DataFrame for a category"""
        cat = category.lower()
        if cat == 'flight':
            return self.data_manager.flights
        elif cat == 'booking':
            return self.data_manager.bookings
        elif cat == 'passenger':
            return self.data_manager.passengers
        elif cat == 'aircraft':
            return self.data_manager.aircraft
        return None

    def get_id_column(self, category):
        """Get the ID column name for a category"""
        id_col_map = {
            "flight": "FlightID",
            "booking": "BookingID",
            "passenger": "PassengerID",
            "aircraft": "AircraftID"
        }
        return id_col_map.get(category.lower())

    # ==================== ADD ENTRY ====================
    
    def add_entry(self, category):
        """Add a new entry to the specified category"""
        category = category.lower()
        df = self.get_dataframe(category)
        id_col = self.get_id_column(category)
        
        if df is None:
            return False, f" Invalid category: {category}"
        
        # CRITICAL: Reset any multi-level indexes that might exist from FlightSearch
        # This ensures the DataFrame has normal columns before we try to add new data
        if category == 'flight' and isinstance(self.data_manager.flights.index, pd.MultiIndex):
            self.data_manager.flights.reset_index(inplace=True)
            # Drop the temporary 'Date' column created by FlightSearch
            if 'Date' in self.data_manager.flights.columns:
                self.data_manager.flights.drop(columns=['Date'], inplace=True)
        
        print(f"\n{'='*50}")
        print(f"ADD NEW {category.upper()}")
        print(f"{'='*50}")
        
        try:
            # Determine next ID
            if df.empty:
                new_id = 1
            else:
                new_id = int(df[id_col].max()) + 1
            
            print(f"New {id_col} will be: {new_id}")
            
            new_row = {id_col: new_id}
            
            # Flight-specific: prompt for AircraftID and auto-fill capacity
            if category == 'flight':
                new_row = self._add_flight_specific(new_row)
                if new_row is None:
                    return False, " Flight creation cancelled."
            
            # Booking-specific: validate flight and passenger exist
            elif category == 'booking':
                new_row = self._add_booking_specific(new_row)
                if new_row is None:
                    return False, " Booking creation cancelled."
            
            # Passenger-specific
            elif category == 'passenger':
                new_row = self._add_passenger_specific(new_row)
                if new_row is None:
                    return False, " Passenger creation cancelled."
            
            # Aircraft-specific
            elif category == 'aircraft':
                new_row = self._add_aircraft_specific(new_row)
                if new_row is None:
                    return False, " Aircraft creation cancelled."
            
            # Add the new row to the DataFrame
            new_df_row = pd.DataFrame([new_row])
            
            if category == 'flight':
                self.data_manager.flights = pd.concat(
                    [self.data_manager.flights, new_df_row], ignore_index=True
                )
                self.data_manager.flight_index[new_id] = new_row
            elif category == 'booking':
                self.data_manager.bookings = pd.concat(
                    [self.data_manager.bookings, new_df_row], ignore_index=True
                )
                self.data_manager.booking_index[new_id] = new_row
            elif category == 'passenger':
                self.data_manager.passengers = pd.concat(
                    [self.data_manager.passengers, new_df_row], ignore_index=True
                )
                self.data_manager.passenger_index[new_id] = new_row
            elif category == 'aircraft':
                self.data_manager.aircraft = pd.concat(
                    [self.data_manager.aircraft, new_df_row], ignore_index=True
                )
                self.data_manager.aircraft_index[new_row['AircraftID']] = new_row
            
            return True, f" Added new {category} with {id_col} = {new_id}"
            
        except Exception as e:
            return False, f" Error adding {category}: {e}"

    def _add_flight_specific(self, new_row):
        """Handle flight-specific input"""
        try:
            # Show available aircraft
            if self.data_manager.aircraft.empty:
                print(" No aircraft available in the system.")
                return None
            
            print("\nAvailable Aircraft:")
            for _, aircraft in self.data_manager.aircraft.iterrows():
                print(f"  {aircraft['AircraftID']} - "
                      f"{aircraft['Rows']} rows x {aircraft['SeatsInARow']} seats = "
                      f"{int(aircraft['Rows']) * int(aircraft['SeatsInARow'])} capacity")
            
            # Get aircraft ID with validation
            while True:
                aircraft_id = input("\nEnter AircraftID: ").strip()
                aircraft = self.data_manager.get_aircraft_by_id(aircraft_id)
                if aircraft is not None:
                    break
                print(" Invalid AircraftID. Please enter a valid one.")
            
            # Auto-fill capacity based on aircraft
            flight_capacity = int(aircraft['Rows']) * int(aircraft['SeatsInARow'])
            
            new_row['AeroplaneNumber'] = aircraft_id
            new_row['FlightCapacity'] = flight_capacity
            
            # Get other flight details
            new_row['DepartureCity'] = input("Departure City: ").strip()
            new_row['ArrivalCity'] = input("Arrival City: ").strip()
            
            # Validate date/time with loop until valid
            while True:
                datetime_str = input("Date/Time (YYYY-MM-DD HH:MM:SS): ").strip()
                valid, datetime_obj, error_msg = self.validate_datetime(datetime_str)
                if valid:
                    new_row['DateTime'] = datetime_str
                    break
                else:
                    if error_msg:
                        print(f" {error_msg}")
                    else:
                        print(" Invalid format. Please use YYYY-MM-DD HH:MM:SS (e.g., 2025-12-25 14:30:00)")
            
            # Validate cost is positive
            while True:
                try:
                    cost = float(input("Cost per Seat (€): "))
                    if cost <= 0:
                        print(" Cost must be greater than 0")
                        continue
                    new_row['CostPerSeat'] = cost
                    break
                except ValueError:
                    print(" Please enter a valid number")
            
            new_row['Status'] = 'Scheduled'
            
            return new_row
            
        except Exception as e:
            print(f" Error: {e}")
            return None

    def _add_booking_specific(self, new_row):
        """Handle booking-specific input with validation"""
        try:
            # Get and validate Flight ID
            flight_id = int(input("Enter Flight ID: ").strip())
            flight = self.data_manager.get_flight_by_id(flight_id)
            if flight is None:
                print(f" Flight ID {flight_id} not found.")
                return None
            if flight['Status'] == 'Cancelled':
                print(f" Flight {flight_id} has been cancelled.")
                return None
            
            # Get and validate Passenger ID
            passenger_id = int(input("Enter Passenger ID: ").strip())
            passenger = self.data_manager.get_passenger_by_id(passenger_id)
            if passenger is None:
                print(f" Passenger ID {passenger_id} not found.")
                return None
            
            # Get seat number
            seat_number = int(input("Enter Seat Number: ").strip())
            
            new_row['FlightID'] = flight_id
            new_row['PassengerID'] = passenger_id
            new_row['SeatNumber'] = seat_number
            new_row['Status'] = 'Booked'
            
            return new_row
            
        except ValueError:
            print(" Invalid input. Please enter numeric values.")
            return None
        except Exception as e:
            print(f" Error: {e}")
            return None

    def _add_passenger_specific(self, new_row):
        """Handle passenger-specific input"""
        try:
            new_row['FirstName'] = input("First Name: ").strip()
            new_row['Surname'] = input("Surname: ").strip()
            
            # Validate Date of Birth
            while True:
                dob_str = input("Date of Birth (YYYY-MM-DD): ").strip()
                valid, dob_obj = self.validate_date(dob_str)
                if valid:
                    # Check if DOB is in the future
                    if dob_obj > datetime.now():
                        print(" Date of birth cannot be in the future")
                        continue
                    # Check if person is too old (e.g., over 120 years)
                    age = (datetime.now() - dob_obj).days / 365.25
                    if age > 120:
                        print(" Invalid date of birth (person would be over 120 years old)")
                        continue
                    new_row['DOB'] = dob_str
                    break
                else:
                    print(" Invalid date format. Please use YYYY-MM-DD (e.g., 1990-05-15)")
            
            # Validate Email
            while True:
                email = input("Email: ").strip()
                valid, error_msg = self.validate_email(email)
                if valid:
                    new_row['Email'] = email
                    break
                else:
                    print(f" {error_msg}. Email must contain @ and a domain (e.g., user@example.com)")
            
            # Validate Phone Number
            while True:
                phone = input("Phone Number: ").strip()
                valid, error_msg = self.validate_phone(phone)
                if valid:
                    new_row['PhoneNumber'] = phone
                    break
                else:
                    print(f" {error_msg}. Please enter at least 7 digits")
            
            new_row['Address'] = input("Address: ").strip()
            
            return new_row
            
        except Exception as e:
            print(f" Error: {e}")
            return None

    def _add_aircraft_specific(self, new_row):
        """Handle aircraft-specific input"""
        try:
            # AircraftID is special - it's a string, not auto-incremented
            aircraft_id = input("Aircraft ID (e.g., A320, B737): ").strip()
            
            # Check if aircraft already exists
            if self.data_manager.get_aircraft_by_id(aircraft_id) is not None:
                print(f" Aircraft {aircraft_id} already exists.")
                return None
            
            new_row['AircraftID'] = aircraft_id
            new_row['Rows'] = int(input("Number of Rows: ").strip())
            new_row['SeatsInARow'] = int(input("Seats per Row: ").strip())
            
            return new_row
            
        except ValueError:
            print(" Invalid input. Please enter numeric values for rows and seats.")
            return None
        except Exception as e:
            print(f" Error: {e}")
            return None

    # ==================== CANCEL ENTRY ====================
    
    def cancel_entry(self, category):
        """Cancel an entry (set status to Cancelled)"""
        category = category.lower()
        df = self.get_dataframe(category)
        id_col = self.get_id_column(category)
        
        if df is None:
            return False, f" Invalid category: {category}"
        
        # CRITICAL: Reset any multi-level indexes that might exist from FlightSearch
        if category == 'flight' and isinstance(self.data_manager.flights.index, pd.MultiIndex):
            self.data_manager.flights.reset_index(inplace=True)
            if 'Date' in self.data_manager.flights.columns:
                self.data_manager.flights.drop(columns=['Date'], inplace=True)
        elif category == 'booking' and isinstance(self.data_manager.bookings.index, pd.MultiIndex):
            self.data_manager.bookings.reset_index(inplace=True)
        
        print(f"\n{'='*50}")
        print(f"CANCEL {category.upper()}")
        print(f"{'='*50}")
        
        try:
            # Ensure Status column exists
            if 'Status' not in df.columns:
                return False, f" {category} does not have a Status column."
            
            entry_num = input(f"Enter {id_col} to cancel: ").strip()
            
            # Handle numeric vs string IDs
            if category == 'aircraft':
                entry_id = entry_num
            else:
                if not entry_num.isdigit():
                    return False, " Invalid ID. Must be a number."
                entry_id = int(entry_num)
            
            # Check if entry exists
            if category == 'flight':
                entry = self.data_manager.get_flight_by_id(entry_id)
                if entry is None:
                    return False, f" {id_col} {entry_id} not found."
                # Update the DataFrame
                self.data_manager.flights.loc[
                    self.data_manager.flights[id_col] == entry_id, 'Status'
                ] = 'Cancelled'
                # Update index
                self.data_manager.flight_index[entry_id]['Status'] = 'Cancelled'
                
            elif category == 'booking':
                entry = self.data_manager.get_booking_by_id(entry_id)
                if entry is None:
                    return False, f" {id_col} {entry_id} not found."
                # Update the DataFrame
                self.data_manager.bookings.loc[
                    self.data_manager.bookings[id_col] == entry_id, 'Status'
                ] = 'Cancelled'
                # Update index
                self.data_manager.booking_index[entry_id]['Status'] = 'Cancelled'
                
            elif category == 'passenger':
                return False, " Passengers cannot be cancelled. Use delete instead."
                
            elif category == 'aircraft':
                return False, " Aircraft cannot be cancelled. Use delete instead."
            
            return True, f" {category.capitalize()} {entry_id} has been cancelled."
            
        except Exception as e:
            return False, f" Error cancelling {category}: {e}"

    # ==================== DELETE ENTRY ====================
    
    def delete_entry(self, category):
        """Permanently delete an entry"""
        category = category.lower()
        df = self.get_dataframe(category)
        id_col = self.get_id_column(category)
        
        if df is None:
            return False, f" Invalid category: {category}"
        
        # CRITICAL: Reset any multi-level indexes that might exist from FlightSearch
        if category == 'flight' and isinstance(self.data_manager.flights.index, pd.MultiIndex):
            self.data_manager.flights.reset_index(inplace=True)
            if 'Date' in self.data_manager.flights.columns:
                self.data_manager.flights.drop(columns=['Date'], inplace=True)
        elif category == 'booking' and isinstance(self.data_manager.bookings.index, pd.MultiIndex):
            self.data_manager.bookings.reset_index(inplace=True)
        elif category == 'passenger' and isinstance(self.data_manager.passengers.index, pd.MultiIndex):
            self.data_manager.passengers.reset_index(inplace=True)
        elif category == 'aircraft' and isinstance(self.data_manager.aircraft.index, pd.MultiIndex):
            self.data_manager.aircraft.reset_index(inplace=True)
        
        print(f"\n{'='*50}")
        print(f"DELETE {category.upper()}")
        print(f"{'='*50}")
        print("  WARNING: This action cannot be undone!")
        
        try:
            entry_num = input(f"Enter {id_col} to delete: ").strip()
            
            # Handle numeric vs string IDs
            if category == 'aircraft':
                entry_id = entry_num
            else:
                if not entry_num.isdigit():
                    return False, " Invalid ID. Must be a number."
                entry_id = int(entry_num)
            
            # Check if entry exists and show details
            if category == 'flight':
                entry = self.data_manager.get_flight_by_id(entry_id)
                if entry is None:
                    return False, f" {id_col} {entry_id} not found."
                print(f"\nFlight: {entry['DepartureCity']} → {entry['ArrivalCity']} on {entry['DateTime']}")
                
                # Check for bookings
                bookings = self.data_manager.get_bookings_for_flight(entry_id)
                if not bookings.empty:
                    print(f"  This flight has {len(bookings)} booking(s).")
                    confirm = input("Type 'DELETE' to confirm deletion of flight AND all bookings: ")
                    if confirm != 'DELETE':
                        return False, "Deletion cancelled."
                    # Delete bookings first
                    self.data_manager.bookings = self.data_manager.bookings[
                        self.data_manager.bookings['FlightID'] != entry_id
                    ].reset_index(drop=True)
                
            elif category == 'booking':
                entry = self.data_manager.get_booking_by_id(entry_id)
                if entry is None:
                    return False, f" {id_col} {entry_id} not found."
                print(f"\nBooking: Flight {entry['FlightID']}, Passenger {entry['PassengerID']}, Seat {entry['SeatNumber']}")
                
            elif category == 'passenger':
                entry = self.data_manager.get_passenger_by_id(entry_id)
                if entry is None:
                    return False, f" {id_col} {entry_id} not found."
                print(f"\nPassenger: {entry['FirstName']} {entry['Surname']}")
                
                # Check for bookings
                passenger_bookings = self.data_manager.bookings[
                    self.data_manager.bookings['PassengerID'] == entry_id
                ]
                if not passenger_bookings.empty:
                    print(f"  This passenger has {len(passenger_bookings)} booking(s).")
                    confirm = input("Type 'DELETE' to confirm deletion of passenger AND all bookings: ")
                    if confirm != 'DELETE':
                        return False, "Deletion cancelled."
                    # Delete bookings first
                    self.data_manager.bookings = self.data_manager.bookings[
                        self.data_manager.bookings['PassengerID'] != entry_id
                    ].reset_index(drop=True)
                
            elif category == 'aircraft':
                entry = self.data_manager.get_aircraft_by_id(entry_id)
                if entry is None:
                    return False, f" {id_col} {entry_id} not found."
                print(f"\nAircraft: {entry['AircraftID']} ({entry['Rows']}x{entry['SeatsInARow']} seats)")
                
                # Check if aircraft is used in any flights
                aircraft_flights = self.data_manager.flights[
                    self.data_manager.flights['AeroplaneNumber'] == entry_id
                ]
                if not aircraft_flights.empty:
                    return False, f" Cannot delete aircraft {entry_id}. It is used in {len(aircraft_flights)} flight(s)."
            
            # Final confirmation if not already done
            if category not in ['flight', 'passenger']:
                confirm = input(f"\nConfirm deletion of {category} {entry_id}? (yes/no): ").lower()
                if confirm != 'yes':
                    return False, "Deletion cancelled."
            
            # Perform deletion
            if category == 'flight':
                self.data_manager.flights = self.data_manager.flights[
                    self.data_manager.flights[id_col] != entry_id
                ].reset_index(drop=True)
                del self.data_manager.flight_index[entry_id]
                
            elif category == 'booking':
                self.data_manager.bookings = self.data_manager.bookings[
                    self.data_manager.bookings[id_col] != entry_id
                ].reset_index(drop=True)
                del self.data_manager.booking_index[entry_id]
                
            elif category == 'passenger':
                self.data_manager.passengers = self.data_manager.passengers[
                    self.data_manager.passengers[id_col] != entry_id
                ].reset_index(drop=True)
                del self.data_manager.passenger_index[entry_id]
                
            elif category == 'aircraft':
                self.data_manager.aircraft = self.data_manager.aircraft[
                    self.data_manager.aircraft[id_col] != entry_id
                ].reset_index(drop=True)
                del self.data_manager.aircraft_index[entry_id]
            
            # Rebuild indexes to ensure consistency
            self.data_manager.rebuild_indexes()
            
            return True, f"  Deleted {category} {entry_id} successfully."
            
        except Exception as e:
            return False, f" Error deleting {category}: {e}"

    # ==================== SAVE DATA ====================
    
    def save_data(self):
        """Save all changes to CSV files"""
        try:
            self.data_manager.save_data()
            return True, " All changes saved successfully."
        except Exception as e:
            return False, f" Error saving data: {e}"

    # ==================== INTERACTIVE MENU ====================
    
    def interactive_menu(self):
        """Interactive admin menu"""
        while True:
            print("\n" + "="*50)
            print("ADMIN MANAGEMENT SYSTEM")
            print("="*50)
            print("\nSelect Action:")
            print("  1. Add Entry")
            print("  2. Cancel Entry")
            print("  3. Delete Entry")
            print("  4. Return to Main Menu")
            
            action = input("\nEnter choice (1-4): ").strip()
            
            if action == '4':
                print("Returning to main menu...")
                break
            
            if action not in ['1', '2', '3']:
                print(" Invalid choice. Please select 1-4.")
                input("\nPress Enter to continue...")
                continue
            
            # Select category
            print("\nSelect Category:")
            print("  1. Flight")
            print("  2. Booking")
            print("  3. Passenger")
            print("  4. Aircraft")
            
            cat_choice = input("\nEnter choice (1-4): ").strip()
            
            category_map = {
                '1': 'flight',
                '2': 'booking',
                '3': 'passenger',
                '4': 'aircraft'
            }
            
            category = category_map.get(cat_choice)
            if not category:
                print(" Invalid category choice.")
                input("\nPress Enter to continue...")
                continue
            
            # Perform action
            success = False
            message = ""
            
            if action == '1':  # Add
                success, message = self.add_entry(category)
            elif action == '2':  # Cancel
                success, message = self.cancel_entry(category)
            elif action == '3':  # Delete
                success, message = self.delete_entry(category)
            
            print(message)
            
            # Ask to save if successful
            if success:
                save = input("\nSave changes to file? (yes/no): ").lower()
                if save == 'yes':
                    success, msg = self.save_data()
                    print(msg)
            
            input("\nPress Enter to continue...")
