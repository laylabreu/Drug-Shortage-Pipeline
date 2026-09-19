##make a request, if it fails, wait and try again a few times before giving up
## NADAC needs this too so instead of making two of these files we are writing them once in a file both scripts import so I only have to fix bugs once.
import time

import requests

MAX_ATTEMPTS=3
INITIAL_WAIT =1

def fetch_retry(url, params):
    for attempts in range(MAX_ATTEMPTS):
        response = requests.get(url, params)
        if response.status_code == 200:
            break
        time.sleep(INITIAL_WAIT*(2**attempts))
    if response.status_code != 200:
        raise Exception(f'Request failed on attempt {MAX_ATTEMPTS}, where status code was {response.status_code}')
    return response.json()









