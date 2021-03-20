import requests

url = "http://localhost:5000/api"

r = requests.get(url = url + "/5")

data = r.json()

print(data)
