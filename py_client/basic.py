import requests

# endpoint = "https://httpbin.org/status/200"
# endpoint = "https://httpbin.org/"

# endpoint = "https://httpbin.org/anything"
endpoint = "http://localhost:8000/api/"

get_response = requests.get(endpoint)
# print(get_response.text)
print(get_response.status_code)
print(get_response.json()['message'])
# get_response = requestxs.get(endpoint, json={"query": "Hello World"})
