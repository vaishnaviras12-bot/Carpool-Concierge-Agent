import time
import json
from pathlib import Path
from typing import List, Dict

# ----------------- File paths -----------------
DRIVERS_FILE = Path("drivers.json")
RIDE_REQUESTS_FILE = Path("ride_requests.json")

# ----------------- Driver Model -----------------
class Driver:
    def __init__(self, id, vehicle, seats, lat, lon, dest_lat, dest_lon, start_time, from_city=None, to_city=None):
        self.id = id
        self.vehicle = vehicle
        self.seats = int(seats)
        self.lat = lat
        self.lon = lon
        self.dest_lat = dest_lat
        self.dest_lon = dest_lon
        self.start_time = start_time
        self.from_city = from_city
        self.to_city = to_city

    def dict(self):
        return {
            "id": self.id,
            "vehicle": self.vehicle,
            "seats": self.seats,
            "lat": self.lat,
            "lon": self.lon,
            "dest_lat": self.dest_lat,
            "dest_lon": self.dest_lon,
            "start_time": self.start_time,
            "from_city": self.from_city,
            "to_city": self.to_city
        }

# ----------------- Global Driver List -----------------
DRIVERS: List[Driver] = []


# ----------------- Save Drivers to JSON -----------------
def save_drivers_to_file():
    data = [d.dict() for d in DRIVERS]
    with open(DRIVERS_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ----------------- Load Drivers from JSON -----------------
def load_drivers_from_file():
    if not DRIVERS_FILE.exists():
        return []
    with open(DRIVERS_FILE, "r") as f:
        return json.load(f)


# ----------------- Seed Demo Drivers -----------------
def seed_demo_drivers(n=10):
    demo_data = [
        {"id": f"Driver{i}", "vehicle": "Sedan", "seats": 4,
         "lat": 28.6139, "lon": 77.2090, "dest_lat": 19.0760, "dest_lon": 72.8777,
         "start_time": int(time.time()) + 900,
         "from_city": "Delhi", "to_city": "Mumbai"} for i in range(1, n+1)
    ]
    for d in demo_data:
        DRIVERS.append(Driver(**d))


# ----------------- Register Driver -----------------
def register_driver(data: Dict):
    driver = Driver(
        id=data["id"],
        vehicle=data["vehicle"],
        seats=data["seats"],
        lat=data["lat"],
        lon=data["lon"],
        dest_lat=data["dest_lat"],
        dest_lon=data["dest_lon"],
        start_time=data["start_time"],
        from_city=data["from_city"],
        to_city=data["to_city"]
    )
    DRIVERS.append(driver)
    save_drivers_to_file()  # persist
    return {"status": "driver_registered", "driver_id": driver.id}


# ----------------- Find Matches -----------------
def find_matches(data: Dict):
    from_city = data.get("from")
    to_city = data.get("to")
    seats_needed = int(data.get("seats", 1))

    matches = []
    for d in DRIVERS:
        if d.from_city == from_city and d.to_city == to_city and d.seats >= seats_needed:
            matches.append(d.dict())

    # Save search request
    ride_request = {
        "id": f"req_{int(time.time()*1000)}",
        "from": from_city,
        "to": to_city,
        "seats": seats_needed,
        "timestamp": int(time.time())
    }
    save_ride_request(ride_request)

    return {"rides": matches}


# ----------------- Save Ride Request -----------------
def save_ride_request(request_data: dict):
    try:
        with open(RIDE_REQUESTS_FILE, "r") as f:
            requests = json.load(f)
    except FileNotFoundError:
        requests = []

    requests.append(request_data)

    with open(RIDE_REQUESTS_FILE, "w") as f:
        json.dump(requests, f, indent=2)


# ----------------- Confirm Ride (lock seats) -----------------
def confirm_ride(driver_id: str, seats_booked: int = 1):
    for d in DRIVERS:
        if d.id == driver_id:
            if d.seats >= seats_booked:
                d.seats -= seats_booked
                save_drivers_to_file()()   # write back to drivers.json
                return True
            return False



# ----------------- Load persistent drivers on import -----------------
persisted = load_drivers_from_file()
for d in persisted:
    DRIVERS.append(Driver(**d))
