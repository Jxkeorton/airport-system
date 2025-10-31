import pandas as pd

class AirportDataOptimized:
    """
    The AirportDataOptimized class manages airport data efficiently.
    It loads Flights, Passengers, Bookings, and Aircraft from CSVs into pandas DataFrames
    and also builds hash map indexes for lookups by ID.
    """

    def __init__(self, flights_path: str, passengers_path: str, bookings_path: str, aircraft_path: str):
        self.flights_path = flights_path
        self.passengers_path = passengers_path
        self.bookings_path = bookings_path
        self.aircraft_path = aircraft_path

        # Load CSV files into DataFrames with type hints for efficiency
        self.flights = pd.read_csv(flights_path, dtype={"FlightID": int, "FlightCapacity": int})
        self.passengers = pd.read_csv(passengers_path, dtype={"PassengerID": int})
        self.bookings = pd.read_csv(bookings_path, dtype={"BookingID": int, "FlightID": int, "PassengerID": int})
        self.aircraft = pd.read_csv(aircraft_path, dtype={"AircraftID": str, "Rows": int, "SeatsInARow": int})

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
        self.flights.to_csv(self.flights_path, index=False)
        self.passengers.to_csv(self.passengers_path, index=False)
        self.bookings.to_csv(self.bookings_path, index=False)
        self.aircraft.to_csv(self.aircraft_path, index=False)
        
    def rebuild_indexes(self):
        """Rebuild all indexes after data modifications. Call after adding/deleting bookings."""
        self.flight_index = {row["FlightID"]: row for row in self.flights.to_dict("records")}
        self.passenger_index = {row["PassengerID"]: row for row in self.passengers.to_dict("records")}
        self.booking_index = {row["BookingID"]: row for row in self.bookings.to_dict("records")}
        self.aircraft_index = {row["AircraftID"]: row for row in self.aircraft.to_dict("records")}
        self.flight_bookings_index = self._build_flight_bookings_index()
