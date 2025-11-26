# agent_main.py
from google.adk import Agent
from tools.ride_matcher import find_matches, register_driver, seed_demo_drivers, DRIVERS
from tools.long_runner import start_long_job, job_status, pause_job, resume_job
import time

SYSTEM_PROMPT = """
You are Carpool Concierge, an AI mobility assistant.
Your job is to:
- Match passengers to drivers
- Help users schedule rides
- Confirm availability, time, and seats
- Use tools instead of making up answers
- Be concise, friendly, and proactive
Never invent drivers or cars. Only use tool results.
If no drivers match, offer alternatives (time change, location radius, etc.).
• Always call ride_matcher.find_matches before responding to a ride request.
• If distance or time is unknown, call Google Search for traffic info.
• Never invent results — rely only on tool outputs.
If you need real-time traffic information, call Google Search tool.
"""

# ----------------- MEMORY CHECK & SEED -----------------
# DRIVERS list is loaded by ride_matcher.py from memory
if not DRIVERS:
    seed_demo_drivers(num_drivers=10)

# ----------------- CREATE AGENT -----------------
def make_agent():
    agent = Agent(name="CarpoolConcierge")
    agent.instruction = SYSTEM_PROMPT

    # Tool mapping
    agent.tools = {
        "ride_matcher.find_matches": find_matches,
        "ride_matcher.register_driver": register_driver,
        "long_runner.start": start_long_job,
        "long_runner.status": job_status,
        "long_runner.pause": pause_job,
        "long_runner.resume": resume_job,
    }

    return agent

if __name__ == "__main__":
    agent = make_agent()
    print("Agent ready. Use the agent.tools dictionary to call tools.")

    # ----------------- TEST CALL -----------------
    # Call tools directly from agent.tools instead of run_tool()
    test_request = {
        "id": "REQ-01",
        "name": "Test User",
        "lat": 28.6139,
        "lon": 77.2090,
        "dest_lat": 28.5355,
        "dest_lon": 77.3910,
        "time": time.time() + 3600,  # 1 hour from now
        "seats_needed": 2
    }

    test_result = agent.tools["ride_matcher.find_matches"](test_request)
    print("Test find_matches result:", test_result)
