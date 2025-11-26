                                                    CARPOOL CONCIERGE AGENT
A simple flask-based ridesharing web platform that allows passengers to search and book carpool rides and allows drivers to register their rides. It features real-time set locking, dynamic pricing ,payment progress simulation , persistent driver storage , ride request history and a draggable chatbot.It enables users to find rides, book seats securely and ravel affordably- while driver earns by sharing empty seats.

Powered by an *AI chatbot* , ORBIS guides users throughout the ride booking process and reduces confusion for first-time visitors.

FEATURES

-Search and book rides.
-View matched drivers instantly.
-Simple origin and destination selection.
-Price updates dynamically based on seats selected.
-Flask based backend.
-Secure payment simulation.
-Seat lock after confirmation i.e. seats reduce with every booking and update automatically on the frontend.
-Store ride requests and drivers registered in ride_requests.json and drivers.json respectively.
-Drivers can register via three-dot menu.
-Floating draggable chatbot providing guidance.
-Smart pre-defined answers for:
     ->ride/drivers
     ->pricing and payment
     ->policies, cancellation, safety etc.
-Payment popup only succeeds after the async job completes.


TECH STACK

-Backend: Flask
-Python
-Frontend: HTML, CSS, JavaScript
-Tools: Uvicorn
-Data persistance: drivers.json and ride_requests.join
-Concurrency: Threads for async confirmation
-UI Extra: Draggable chatbot & payment popup.



PROJECT STRUCTURE

carpool_agent/
│
├─ app.py                     # Main Flask backend server
├─ requirements.txt           # Project dependencies
├─ README.md                  # Project documentation
│
├─ drivers.json               # Persistent database — registered drivers
├─ ride_requests.json         # Persistent database — ride search and bookings
│
├─ templates/
│   └─ index.html             # UI — main interface (chatbot + ride search + driver reg)
│
└─ tools/
    ├─ ride_matcher.py        # Core matching logic + seat deduction + pricing
    ├─ memory_store.py        # JSON read/write helper (persistent storage)
    ├─ long_runner.py         # Background task runner
    ├─ matching.py    



HOW TO RUN 

-Install dependencies 
pip install flask 

-Run the flask server 
python app.py

-open the link in browser
http://127.0.0.1:5000/



DATA STORAGE
drivers.jsons stores persistent list of registered drivers.
ride_requests.json stores history of user search queries.



AI CHATBOT COMMANDS
   User query                                     Bot responses
   "ride"                                         Shows how to search rides.
   "book" or "confirm"                            Explains booking and seat lock.
   "driver"                                       Tells where to register.
   "payment"                                      Explains transaction rules.
   "safety"                                       Provides driver's information.
   "contact/help/support"                         Shows contact information.
   "location/pickup"                              Shows live pickup location.
   "refund"                                       Tells about refund process.
   "policy"                                       Tells about travel policy.
  



FUTURE IMPROVEMENTS
-OTP verification.
-Push notifications.
-Rating and reviews.
-Live driver tracking on map.
-In-app chat between driver and rider.
-Multi stop ride matching.