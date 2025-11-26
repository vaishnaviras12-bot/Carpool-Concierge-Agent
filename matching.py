# tools/matching.py
import threading
from math import radians, cos, sin, asin, sqrt

# Thread-safe driver storage
_drivers = []
_lock = threading.Lock()

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance in kilometers between two points."""
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km

def register_driver(lat, lon, start_time, seats, vehicle, driver_id):
    """Register a driver in a thread-safe manner."""
    if not all(isinstance(x, (int, float)) for x in [lat, lon]):
        return {"error": "lat/lon must be numbers"}
    if not isinstance(seats, int) or seats <= 0:
        return {"error": "seats must be a positive integer"}
    if not isinstance(driver_id, str):
        return {"error": "driver_id must be a string"}

    driver = {
        "driver_id": driver_id,
        "lat": lat,
        "lon": lon,
        "start_time": start_time,
        "seats": seats,
        "vehicle": vehicle
    }

    with _lock:
        _drivers.append(driver)

    return {"status": "registered", "driver_id": driver_id}

def update_driver_location(driver_id, new_lat, new_lon):
    """Update a driver's location."""
    if not all(isinstance(x, (int, float)) for x in [new_lat, new_lon]):
        return {"error": "lat/lon must be numbers"}

    with _lock:
        for driver in _drivers:
            if driver["driver_id"] == driver_id:
                driver["lat"] = new_lat
                driver["lon"] = new_lon
                return {"status": "updated", "driver_id": driver_id}

    return {"error": "driver not found"}

def remove_driver(driver_id):
    """Remove a driver from the system."""
    with _lock:
        for i, driver in enumerate(_drivers):
            if driver["driver_id"] == driver_id:
                _drivers.pop(i)
                return {"status": "removed", "driver_id": driver_id}

    return {"error": "driver not found"}

def find_matches(lat, lon, dest_lat, dest_lon, time, seats_needed, max_distance_km=5, top_n=5):
    """
    Find up to `top_n` drivers with enough seats, compatible time,
    and within `max_distance_km` of the pickup location.
    """
    matches = []

    with _lock:
        for driver in _drivers:
            if driver["seats"] < seats_needed:
                continue
            if abs(driver["start_time"] - time) > 3600:  # 1 hour window
                continue
            distance = haversine(lat, lon, driver["lat"], driver["lon"])
            if distance > max_distance_km:
                continue

            matches.append({
                "driver_id": driver["driver_id"],
                "vehicle": driver["vehicle"],
                "pickup_lat": driver["lat"],
                "pickup_lon": driver["lon"],
                "time": driver["start_time"],
                "seats_available": driver["seats"],
                "distance_km": round(distance, 2)
            })

    # Sort by distance
    matches.sort(key=lambda x: x["distance_km"])
    return {"matched": bool(matches), "drivers": matches[:top_n]} if matches else {"matched": False, "reason": "no suitable drivers found"}
