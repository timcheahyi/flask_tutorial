import requests

BASE = "http://localhost:5000/"

res = requests.post(BASE + "video/1", {"likes":10})
print(res.json())