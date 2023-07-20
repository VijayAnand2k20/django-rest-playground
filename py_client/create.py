import requests

headers = {
    "Authorization": "Bearer dfef1fda29f86ef29e058bc1e681ecf86eb2bd62"
}

endpoint = "http://localhost:8000/api/products/"

data = {
    "title": "This is a new product",
}
get_response = requests.post(endpoint, data=data, headers=headers)

print(get_response.json())