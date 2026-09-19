
import requests

from api_client import fetch_retry


def fetch_shortages():
    OPENFDA_API_URL = "https://api.fda.gov/drug/shortages.json"
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
    return len(record_list)


   