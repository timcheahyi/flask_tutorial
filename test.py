import requests

BASE = "http://localhost:5000/"

res = requests.post(BASE)
print(res.json())