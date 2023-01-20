import time

from fastapi import FastAPI, HTTPException

START_PERIOD = 20


app = FastAPI()


@app.get("/")
def periodic_response(period: int):
    if period > 1000:
        raise HTTPException(status_code=500, detail="Service is failing")
    
    time.sleep(period / 1000)
    return f"Service is responding"
