import requests
import json
import pprint
import os
from dotenv import load_dotenv
# Load the environment variables from the .env file
load_dotenv()

# Get the access tokens from the environment variables
source_access_token = os.environ.get('SOURCE_ACCESS_TOKEN')
target_access_token = os.environ.get('TARGET_ACCESS_TOKEN')

#get the hosts from the environment variables
source_host = os.environ.get('SOURCE_HOST_REST_API_URL')
target_host = os.environ.get('TARGET_HOST_REST_API_URL')

# Define the REST API endpoints for both Magento instances
source_api_url = source_host + '/products/attributes?search_criteria[page_size]=1000'
target_api_url = target_host + '/products/attributes?search_criteria[page_size]=1000'

# Set up the authentication headers for both API endpoints
source_headers = {
    'Authorization': f'Bearer {source_access_token}',
    'Content-Type': 'application/json'
}

target_headers = {
    'Authorization': f'Bearer {target_access_token}',
    'Content-Type': 'application/json'
}

# Get the list of attributes from the source Magento instance
print(source_api_url)
source_response = requests.get(source_api_url, headers=source_headers)
source_attributes = json.loads(source_response.text)
source_attributes = source_attributes['items']
# Save the list of source attributes to a JSON file
with open('./data/source_attributes.json', 'w') as outfile:
    json.dump(source_attributes, outfile, indent=4)

# Get the list of attributes from the target Magento instance
target_response = requests.get(target_api_url, headers=target_headers)
target_attributes = json.loads(target_response.text)
target_attributes = target_attributes['items']
# Save the list of target attributes to a JSON file
with open('./data/target_attributes.json', 'w') as outfile:
    json.dump(target_attributes, outfile, indent=4)

# Find the difference between the source and target attributes
source_attr_set = set(attr['attribute_code'] for attr in source_attributes)
target_attr_set = set(attr['attribute_code'] for attr in target_attributes)

diff = source_attr_set.symmetric_difference(target_attr_set)

# Print the difference
print('Attributes missing in target instance:')
pprint.pprint([attr['attribute_code'] for attr in source_attributes if attr['attribute_code'] in diff])
#save the difference to a file
with open('./data/missing_attributes.json', 'w') as outfile:
    json.dump([attr for attr in source_attributes if attr['attribute_code'] in diff], outfile, indent=4)
print('\nAttributes missing in source instance:')
pprint.pprint([attr['attribute_code'] for attr in target_attributes if attr['attribute_code'] in diff])
