import requests
import json
import pandas as pd



# Endpoint URL for ad search
url = "https://jobsearch.api.jobtechdev.se/search"

# Search phrase
search_text = "stockholm"

# Headers for authentication
headers = {
    "api-key": "YOUR_API_KEY",
    "accept": "application/json",
}

# Parameters for search query
params = {
    "q": search_text,
    "limit": 20,  # Number of results to return
}

# Send GET request to the API
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 100:
    # Print the response content in the terminal .json format
    #print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    ""

else:
    print(f"Error: {response.status_code}")




df = pd.DataFrame(response.json()['hits'])
print(df)