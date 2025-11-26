import json
from pathlib import Path

DRIVERS_FILE = Path("drivers.json")
RIDE_REQUESTS_FILE = Path("ride_requests.json")


# ----------------- Load Drivers -----------------
def get_all_drivers():
    if not DRIVERS_FILE.exists():
        return []
    with open(DRIVERS_FILE, "r") as f:
        return json.load(f)


# ----------------- Save Driver -----------------
def save_driver(driver_data):
    drivers = get_all_drivers()
    # Remove duplicate id if exists
    drivers = [d for d in drivers if d["id"] != driver_data["id"]]
    drivers.append(driver_data)
    with open(DRIVERS_FILE, "w") as f:
        json.dump(drivers, f, indent=2)


# ----------------- Load Ride Requests -----------------
def get_all_ride_requests():
    if not RIDE_REQUESTS_FILE.exists():
        return []
    with open(RIDE_REQUESTS_FILE, "r") as f:
        return json.load(f)


# ----------------- Save Ride Request -----------------
def save_ride_request(request_data: dict):
    ride_requests = get_all_ride_requests()
    ride_requests.append(request_data)
    with open(RIDE_REQUESTS_FILE, "w") as f:
        json.dump(ride_requests, f, indent=2)
