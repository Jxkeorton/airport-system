import csv
from datetime import datetime

# Flight class to represent a flight
class Flight:
    def __init__(self, flight_id, departure_city, arrival_city, date_time, passenger_total, flight_capacity):
        self.flight_id = flight_id
        self.departure_city = departure_city
        self.arrival_city = arrival_city
        self.date_time = datetime.fromisoformat(date_time)
        self.passenger_total = int(passenger_total)
        self.flight_capacity = int(flight_capacity)

    def is_available(self):
        return self.passenger_total < self.flight_capacity

    def __str__(self):
        return f"Flight {self.flight_id}: {self.departure_city} -> {self.arrival_city} at {self.date_time}"

# FlightManager to handle loading flights from CSV
class FlightManager:
    def __init__(self, csv_file):
        self.flights = self.load_flights(csv_file)

    def load_flights(self, csv_file):
        flights = []
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                flights.append(Flight(
                    flight_id=row['FlightID'],
                    departure_city=row['DepartureCity'],
                    arrival_city=row['ArrivalCity'],
                    date_time=row['DateTime'],
                    passenger_total=row['PassengerTotal'],
                    flight_capacity=row['FlightCapacity']
                ))
        return flights