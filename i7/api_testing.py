import requests
import json
from collections import defaultdict

if __name__ == "__main__":
    url = 'https://8881-71-212-151-137.ngrok-free.app/page/Product'
    headers = {'Content-Type': 'application/json'}
    
    # Sending a GET request
    response = requests.get(url, headers=headers)
    
    desired_URI = [x for x in response.json()['results']['bindings'] if x['label']['value'] == "Product (business)"][0]['entity']['value']
    print("Desired URI:", desired_URI)

    # Sending a GET request to the resource endpoint
    resource_url = f'https://8881-71-212-151-137.ngrok-free.app/resource?uri={desired_URI}'
    resource_response = requests.get(resource_url, headers=headers)
    print(resource_response)

    #results = get_resource_from_uri(desired_URI)
    #json_results = results
    #test = rdf_to_markdown_grouped(json_results)

    with open('output.md', 'w') as md_file:
        md_file.write(resource_response.content.decode('utf-8'))


    # Checking the response status code
    if response.status_code == 200:
        print("Success!")
        #print("Response JSON:", json.dumps(response.json(), indent=2))
    else:
        print("Error:", response.status_code)
        print("Response Text:", response.text)

