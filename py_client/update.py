import requests

endpoint = "http://localhost:8000/api/products/1/update/"

data = {
    "title": "Hello New World",
    "price": 1299.99
}

get_response = requests.put(endpoint, json=data)

print(get_response.json())