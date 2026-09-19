# #matching counts doesnt prove matching records so if skip misbehaved, 
# # I could have gotten page 1 17 times and still landed on 1613 total.  
# # This is why we check for duplicatees
# ndcs = []
# for record in record_list:
#     ndcs.append(record['package_ndc'])
# print(f'total after removed duplicates NDCs: {len(set(ndcs))}')

# #37 appear more than once so lets see whats going on...

# target = '25021-311-04'
# for record in record_list:
#     if record['package_ndc'] == target:
#         print(record)
# # some products are doubled because of events such as one presentation shows
# #  it as current with the initial posting date, and the duplicate presentation
# #  shows it as discontinuiing.
# #This means I have to look not just at the package_ndc, but the package_ndc + status





# target= '65862-618-90'
# for record in record_list:
#     if record['package_ndc'] == target:
#         print(record)
    
# #So whenever the error fires, skip_counter holds whatever value it had at 
# # that moment. If page 9 fails, the message prints skip=800, and you know the 
# # failure happened on the ninth request, covering records 801 through 900.



# todays_date = datetime.now(timezone.utc).date()

# filename= f'shortage_{todays_date}.json'
# with open(filename, 'w') as f:
#     json.dump(record_list, f, indent=2)
# composite_keys= []
# for record in record_list:
#     composite_keys.append((record['package_ndc'], record['initial_posting_date'], record['status'], record['presentation']))
# print(f'Total records: {len(record_list)}')
# print(f'Unique Composite Keys: {len(set(composite_keys))}')


# key = Counter(composite_keys)
# repeated= []
# for composite_keys,n in key.items():
#     if n >1:
#         repeated.append(composite_keys)

# print(f'repeated NDCs: {len(repeated)}')
# print(repeated[:5])
# counts = Counter(ndcs)
# repeated= []
# for ndc,n in counts.items():
#     if n >1:
#         repeated.append(ndc)

# print(f'repeated NDCs: {len(repeated)}')
# print(repeated[:5])
