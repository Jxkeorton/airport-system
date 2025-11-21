import pandas as pd

class AirportData:
    """
    The AirportData class manages airport data efficiently.
    It loads Flights, Passengers, Bookings, and Aircraft from CSVs into pandas DataFrames
    and also builds hash map indexes for lookups by ID.
    """
    def __init__(self, flights_path: str, passengers_path: str, bookings_path: str, aircraft_path: str):
        self.flights_path = flights_path
        self.passengers_path = passengers_path
        self.bookings_path = bookings_path
        self.aircraft_path = aircraft_path
        
        # Load CSV files into DataFrames
        # NOTE: Removed dtype parameter to avoid any potential column issues
        self.flights = pd.read_csv(flights_path)
        self.passengers = pd.read_csv(passengers_path)
        self.bookings = pd.read_csv(bookings_path)
        self.aircraft = pd.read_csv(aircraft_path)
        
        # Debug: Print what columns were loaded
        print(f"DEBUG - Flights columns loaded: {self.flights.columns.tolist()}")
        print(f"DEBUG - First flight: {self.flights.iloc[0].to_dict() if len(self.flights) > 0 else 'No flights'}")
        
        # Convert types after loading to ensure all columns are preserved
        self.flights['FlightID'] = self.flights['FlightID'].astype(int)
        if 'FlightCapacity' in self.flights.columns:
            self.flights['FlightCapacity'] = self.flights['FlightCapacity'].astype(int)
        
        self.passengers['PassengerID'] = self.passengers['PassengerID'].astype(int)
        
        self.bookings['BookingID'] = self.bookings['BookingID'].astype(int)
        self.bookings['FlightID'] = self.bookings['FlightID'].astype(int)
        self.bookings['PassengerID'] = self.bookings['PassengerID'].astype(int)
        
        if 'Rows' in self.aircraft.columns:
            self.aircraft['Rows'] = self.aircraft['Rows'].astype(int)
        if 'SeatsInARow' in self.aircraft.columns:
            self.aircraft['SeatsInARow'] = self.aircraft['SeatsInARow'].astype(int)
        
        # Build hash map indexes for fast O(1) lookups
        self.flight_index = {row["FlightID"]: row for row in self.flights.to_dict("records")}
        self.passenger_index = {row["PassengerID"]: row for row in self.passengers.to_dict("records")}
        self.booking_index = {row["BookingID"]: row for row in self.bookings.to_dict("records")}
        self.aircraft_index = {row["AircraftID"]: row for row in self.aircraft.to_dict("records")}
        
        # Build flight-to-bookings index for O(b) booking queries per flight
        # This maps flight_id -> list of DataFrame row indices
        self.flight_bookings_index = self._build_flight_bookings_index()
    
    def _build_flight_bookings_index(self):
        """Build an index mapping flight_id to booking row indices for queries"""
        flight_bookings = {}
        for idx, booking in self.bookings.iterrows():
            flight_id = int(booking['FlightID'])
            if flight_id not in flight_bookings:
                flight_bookings[flight_id] = []
            flight_bookings[flight_id].append(idx)
        return flight_bookings
    
    # Flight methods
    def get_flight_by_id(self, flight_id: int):
        return self.flight_index.get(flight_id)
    
    # Passenger methods
    def get_passenger_by_id(self, passenger_id: int):
        return self.passenger_index.get(passenger_id)
    
    # Booking methods
    def get_booking_by_id(self, booking_id: int):
        return self.booking_index.get(booking_id)
    
    def get_bookings_for_flight(self, flight_id: int):
        """Get all bookings for a specific flight."""
        booking_indices = self.flight_bookings_index.get(flight_id, [])
        if not booking_indices:
            # Return empty DataFrame with correct structure
            return pd.DataFrame(columns=self.bookings.columns)
        return self.bookings.iloc[booking_indices]
    
    # Aircraft methods
    def get_aircraft_by_id(self, aircraft_id: str):
        return self.aircraft_index.get(aircraft_id)
    
    # Save all DataFrames back to CSV
    def save_data(self):
        """Save all dataframes to CSV files with verification"""
        # Debug: Print columns before saving
        print(f"\nDEBUG - Saving data...")
        print(f"Flights columns before save: {self.flights.columns.tolist()}")
        print(f"Flights shape: {self.flights.shape}")
        if len(self.flights) > 0:
            print(f"First flight before save: {self.flights.iloc[0].to_dict()}")
        
        # Save all DataFrames
        self.flights.to_csv(self.flights_path, index=False)
        self.passengers.to_csv(self.passengers_path, index=False)
        self.bookings.to_csv(self.bookings_path, index=False)
        self.aircraft.to_csv(self.aircraft_path, index=False)
        
        # Debug: Read back and verify
        verify = pd.read_csv(self.flights_path)
        print(f"Flights columns after save: {verify.columns.tolist()}")
        if len(verify) > 0:
            print(f"First flight after save: {verify.iloc[0].to_dict()}")
        print(f"Save completed successfully.\n")
        
    def rebuild_indexes(self):
        """Rebuild all indexes after data modifications. Call after adding/deleting bookings."""
        self.flight_index = {row["FlightID"]: row for row in self.flights.to_dict("records")}
        self.passenger_index = {row["PassengerID"]: row for row in self.passengers.to_dict("records")}
        self.booking_index = {row["BookingID"]: row for row in self.bookings.to_dict("records")}
        self.aircraft_index = {row["AircraftID"]: row for row in self.aircraft.to_dict("records")}
        self.flight_bookings_index = self._build_flight_bookings_index()