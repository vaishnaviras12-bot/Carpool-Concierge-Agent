import asyncio
import uuid

JOBS = {}

async def _simulate_wait(request_id, duration_sec):
    start = asyncio.get_event_loop().time()
    end = start + duration_sec
    while True:
        now = asyncio.get_event_loop().time()
        remaining = end - now
        if remaining <= 0:
            break
        wait_time = min(0.5, remaining)
        await JOBS[request_id]["pause_event"].wait()
        await asyncio.sleep(wait_time)
    JOBS[request_id]["status"] = "completed"
    JOBS[request_id]["result"] = {"message": "driver_confirmed", "request_id": request_id}

def start_long_job(duration_sec=30):
    request_id = str(uuid.uuid4())
    pause_event = asyncio.Event()
    pause_event.set()
    JOBS[request_id] = {"status": "running", "result": None, "pause_event": pause_event}
    asyncio.create_task(_simulate_wait(request_id, duration_sec))
    return {"job_id": request_id, "status": "started"}

def pause_job(job_id):
    job = JOBS.get(job_id)
    if job and job["status"] == "running":
        job["status"] = "paused"
        job["pause_event"].clear()
        return {"status": "paused", "job_id": job_id}
    return {"error": "not found or not running"}

def resume_job(job_id):
    job = JOBS.get(job_id)
    if job and job["status"] == "paused":
        job["status"] = "running"
        job["pause_event"].set()
        return {"status": "resumed", "job_id": job_id}
    return {"error": "not found or not paused"}

def job_status(job_id):
    job = JOBS.get(job_id)
    if not job:
        return {"error": "not found"}
    return {"job_id": job_id, "status": job["status"], "result": job["result"]}
