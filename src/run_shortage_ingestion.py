
import json
import os
from datetime import datetime, timezone

import requests

from api_client import fetch_retry

OPENFDA_API_URL = "https://api.fda.gov/drug/shortages.json"
OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'output')
PAGE_SIZE = 100
def fetch_shortages():
    
    openFDA_response = requests.get(
    OPENFDA_API_URL, {"limit" : 100,
                    'skip': 0})
    print(f"Status code: {openFDA_response.status_code}")
    shortage_data = openFDA_response.json()
    print(f"Total Shortage Presentations {shortage_data["meta"]["results"]["total"]}")
    print(f"number of records returned: {len(shortage_data['results'])}")
    print(f'Package_ndc of first record:{shortage_data['results'][0]['package_ndc']}')

    record_list = []
    skip_counter = 0
    while len(record_list) < shortage_data['meta']['results']['total'] :
        
        
        shortage_data = fetch_retry(OPENFDA_API_URL,{"limit" : 100,
                    'skip': skip_counter} )
        record_list += shortage_data['results']
        skip_counter+=100
    todays_date = datetime.now(timezone.utc).date()
    filename = os.path.join(OUTPUT_DIR, f'shortage_{todays_date}.json')
    with open(filename, 'w') as f:
        json.dump(record_list, f, indent=2)
    print(f'Wrote {len(record_list)} records to {filename}')


    return len(record_list)


   