import logging
import time

import requests
from pybreaker import CircuitBreaker

from log_listener import LogListener

cb = CircuitBreaker(
    fail_max=3, 
    reset_timeout=5,
    listeners=[LogListener()]
)


@cb
def make_request(period: int):
    response = requests.get(f'http://localhost:8000?period={period}')
    if response.status_code != 200:
        raise Exception("API call failed. CB Fail counter: {cb.fail_counter}")
    return response.json()


def retry_call(max_retries=13, delay=2):
    retry_count = 0
    while retry_count <= max_retries:
        try:
            period = 1220

            if 3 <= retry_count <= 7:
                period = 20

            logging.info(make_request(period))
            retry_count += 1
        except Exception as e:
            logging.error(e)
            if retry_count < max_retries:
                time.sleep(delay)
                retry_count += 1
            else:
                logging.error("Max retries exceeded")
                break

 
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s - %(message)s',
        datefmt='%H:%M:%S',
    )
    
    try:
        retry_call()
    except:
        pass
        