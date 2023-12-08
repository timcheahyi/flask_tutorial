import requests

BASE = "http://localhost:5000/"

# res = requests.post(BASE + "video/1/", {
#     "name" : "video1",
#     "views": 12,
#     "likes": 2
# })

res = requests.get(BASE + "video/1")

print(res.json())