import requests


req_url = "https://www.chinaamc.com/indexfundvalue.js"

response = requests.get(req_url)
print(response.apparent_encoding)
response.encoding = "UTF-8"

print(response.text)