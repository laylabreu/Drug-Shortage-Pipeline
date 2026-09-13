import json
import time
from collections import Counter
from datetime import datetime, timezone

import requests

OPENFDA_API_URL = "https://api.fda.gov/drug/shortages.json"
openFDA_response = requests.get(
OPENFDA_API_URL, {"limit" : 100,
                  'skip': 100})
MAX_ATTEMPTS=3
INITIAL_WAIT =1
print(f"Status code: {openFDA_response.status_code}")
shortage_data = openFDA_response.json()
print(f"Total Shortage Presentations {shortage_data["meta"]["results"]["total"]}")
print(f"number of records returned: {len(shortage_data['results'])}")
print(f'Package_ndc of first record:{shortage_data['results'][0]['package_ndc']}')

record_list = []
skip_counter = 0
while len(record_list) < shortage_data['meta']['results']['total'] :
    for attempt in range(MAX_ATTEMPTS):
        openFDA_response = requests.get(
    OPENFDA_API_URL, {"limit" : 100,
                    'skip': 100})
        if openFDA_response.status_code == 200:
            break
        time.sleep(INITIAL_WAIT*(2**attempt))  
    if openFDA_response.status_code != 200:
        raise Exception(f"Failed after {MAX_ATTEMPTS} attempts at skip {skip_counter}, status {openFDA_response.status_code}")
    
    
    openFDA_response = requests.get(OPENFDA_API_URL, {"limit" : 100, 'skip': skip_counter})
    shortage_data = openFDA_response.json()
    record_list += shortage_data['results']
    skip_counter+=100

print(len(record_list))
#matching counts doesnt prove matching records so if skip misbehaved, 
# I could have gotten page 1 17 times and still landed on 1613 total.  
# This is why we check for duplicatees
ndcs = []
for record in record_list:
    ndcs.append(record['package_ndc'])
print(f'total after removed duplicates NDCs: {len(set(ndcs))}')

#37 appear more than once so lets see whats going on...
counts = Counter(ndcs)
repeated= []
for ndc,n in counts.items():
    if n >1:
        repeated.append(ndc)

print(f'repeated NDCs: {len(repeated)}')
print(repeated[:5])

target = '25021-311-04'
for record in record_list:
    if record['package_ndc'] == target:
        print(record)
# some products are doubled because of events such as one presentation shows
#  it as current with the initial posting date, and the duplicate presentation
#  shows it as discontinuiing.
#This means I have to look not just at the package_ndc, but the package_ndc + status

composite_keys= []
for record in record_list:
    composite_keys.append((record['package_ndc'], record['initial_posting_date'], record['status'], record['presentation']))
print(f'Total records: {len(record_list)}')
print(f'Unique Composite Keys: {len(set(composite_keys))}')



counts = Counter(composite_keys)
repeated= []
for composite_keys,n in counts.items():
    if n >1:
        repeated.append(composite_keys)

print(f'repeated NDCs: {len(repeated)}')
print(repeated[:5])

target= '65862-618-90'
for record in record_list:
    if record['package_ndc'] == target:
        print(record)
    
#So whenever the error fires, skip_counter holds whatever value it had at 
# that moment. If page 9 fails, the message prints skip=800, and you know the 
# failure happened on the ninth request, covering records 801 through 900.



todays_date = datetime.now(timezone.utc).date()

filename= f'shortage_{todays_date}.json'
with open(filename, 'w') as f:
    json.dump(record_list, f, indent=2)


