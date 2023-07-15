import requests

endpoint = "http://localhost:8000/api/products/"

data = {
    "title": "This is a new product",
}
get_response = requests.post(endpoint, data=data)

print(get_response.json())