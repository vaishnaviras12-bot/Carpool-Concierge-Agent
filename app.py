from flask import Flask, request, jsonify, render_template
import time
import threading
import uuid
from tools.ride_matcher import DRIVERS, seed_demo_drivers, register_driver, find_matches, confirm_ride , save_drivers_to_file
from tools.memory_store import save_ride_request, get_all_ride_requests

app = Flask(__name__)

# ---------------- Seed Demo Drivers ----------------
seed_demo_drivers(5)  # Optional: seed demo drivers on startup

# ---------------- Job Queue ----------------
JOB_STATUS = {}  # job_id -> status

# ---------------- Serve Frontend ----------------
@app.route("/")
def index():
    return render_template("index.html")  # Ensure index.html is in 'templates/' folder


# ---------------- Endpoint: Get All Drivers ----------------
@app.route("/get_drivers")
def get_drivers():
    return jsonify({"drivers": [d.dict() for d in DRIVERS]})


# ---------------- Endpoint: Register Driver ----------------
@app.route("/register_driver", methods=["POST"])
def register_driver_endpoint():
    data = request.json
    result = register_driver(data)
    return jsonify(result)


# ---------------- Endpoint: Search Rides ----------------
@app.route("/search_rides", methods=["POST"])
def api_search_rides():
    data = request.json
    result = find_matches(data)

    # Store user ride request
    ride_request = {
        "id": f"req_{int(time.time()*1000)}",
        "user_name": data.get("user_name"),
        "from_city": data.get("from"),
        "to_city": data.get("to"),
        "seats": data.get("seats"),
        "timestamp": int(time.time())
    }
    save_ride_request(ride_request)

    return jsonify(result)



# ---------------- Endpoint: Confirm Ride (Async) ----------------
def confirm_ride(driver_id: str, seats_booked: int = 1):
    for d in DRIVERS:
        if d.id == driver_id:
            if d.seats >= seats_booked:
                d.seats -= seats_booked
                save_drivers_to_file()  # write back to drivers.json
                return True
            return False

JOB_STATUS = {}

@app.route("/confirm_ride", methods=["POST"])
def confirm_ride_job():
    data = request.json
    driver_id = data.get("driver_id")
    seats = int(data.get("seats", 1))
    job_id = str(uuid.uuid4())
    JOB_STATUS[job_id] = "processing"

    def job():
        time.sleep(2)  # simulate delay
        success = confirm_ride(driver_id, seats)
        JOB_STATUS[job_id] = "completed" if success else "failed"

    threading.Thread(target=job).start()
    return jsonify({"job_id": job_id})

# ---------------- Endpoint: Poll Job Status ----------------
@app.route("/job_status/<job_id>")
def job_status(job_id):
    status = JOB_STATUS.get(job_id, "unknown")
    return jsonify({"status": status})


# ---------------- Endpoint: Lock Seats ----------------
@app.route("/lock_seats", methods=["POST"])
def lock_seats():
    data = request.json
    driver_id = data.get("driver_id")
    seats = int(data.get("seats", 1))
    success = confirm_ride(driver_id, seats)
    return jsonify({"status": "locked" if success else "failed"})


# ---------------- Endpoint: Save Ride Request ----------------
@app.route("/save_ride_request", methods=["POST"])
def save_ride_request_endpoint():
    ride = request.json
    save_ride_request(ride)
    return jsonify({"status": "saved"})


@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message", "").lower()

    if any(word in msg for word in ["hi", "hello", "hey"]):
        reply = "Hello! I'm ORBIS. Please type ride/driver/book/confirm/cancel/\npayment/safety/contact/\nsupport/help/policy/pickup/late according to your convenience."

    elif "ride" in msg :
        reply = "To search a ride, select *From*, *To* and *Seats* then tap `Find Rides`."

    elif "book" in msg or "confirm" in msg:
        reply = "After selecting a ride, click *Confirm*. A secure payment check runs, then your seat gets locked ⏳"

    elif "driver" in msg :
        reply = "Drivers can register by clicking the three dots (⋮) in the top-right → `Register as Driver` 🚕"

    elif "cancel" in msg:
        reply = "You may cancel your ride anytime. Refund depends on driver policy — usually full refund if cancelled before pickup ⏱"

    elif "payment" in msg or "price" in msg or "cost" in msg:
        reply = "Payments are processed securely. Price depends on distance & seats selected 💳"

    elif "safety" in msg:
        reply = "Safety first! You’ll see the driver’s profile, car number, and contact before pickup ✔"

    elif "contact" in msg or "support" in msg or "help" in msg:
        reply = "You can message support anytime: support@orbis-rides.com 📩"

    elif "where" in msg or "location" in msg or "pickup" in msg:
        reply = "Once a ride is booked, the live pickup location becomes visible in your dashboard 📍"

    elif "refund" in msg:
        reply = "Refunds normally take 3–5 business days back to your original payment method 💸"

    elif "rules" in msg or "policy" in msg:
        reply = "Drivers and riders must follow our polite travel policy — no smoking, no harassment, respect time & privacy 🤝"

    elif  "late" in msg or "delay" in msg:
        reply = "If the driver is late, you’ll get live ETA updates. ⏳"

    elif "thanks" in msg or "thank you" in msg:
        reply = "I’m always happy to help 😊 Let me know if you'd like to book a ride or register as driver."

    else:
        reply = "I'm not sure about that 🤔 Try asking about rides, drivers, price, safety, payment, refund, pickup or help."

    return jsonify({"reply": reply})



if __name__ == "__main__":
    app.run(debug=True)
