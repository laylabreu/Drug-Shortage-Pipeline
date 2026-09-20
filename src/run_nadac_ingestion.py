
import json
import os
from datetime import datetime, timezone

from api_client import fetch_retry

NADAC_API_URL = 'https://data.medicaid.gov/api/1/datastore/query/fbb83258-11c7-47f5-8b18-5f8e79f7e704/0'
OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'output')
PAGE_SIZE = 8000

def fetch_nadac():
    nadac_response = fetch_retry(NADAC_API_URL, {'limit' : PAGE_SIZE, 'offset' : 0})
    records_list = []
    offset_count = 0
    while len(records_list) < nadac_response['count']:
        nadac_response = fetch_retry(NADAC_API_URL, {'limit' : PAGE_SIZE, 'offset' : offset_count})
        offset_count +=PAGE_SIZE
        records_list += nadac_response['results']
        
    todays_date = datetime.now(timezone.utc).date()
    filename = os.path.join(OUTPUT_DIR, f'nadac_{todays_date}.json')
    with open(filename, 'w') as f:
        json.dump(records_list, f, indent = 2)
    print(f'Wrote {len(records_list)} to {filename}') 
    return len(records_list)
















