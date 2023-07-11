import requests

endpoint = "https://httpbin.org/status/200"
# endpoint = "https://httpbin.org/"

# endpoint = "https://httpbin.org/anything"

get_response = requests.get(endpoint)
# get_response = requests.get(endpoint, json={"query": "Hello World"})

print(get_response.status_code)