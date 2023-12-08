import requests
import json
URL = "http://127.0.0.1:8000/createstudent/"

data = {
    'name': 'aradhya',
    'roll': 111,
    'city': 'Bengaluru'
}
json_data = json.dumps(data)
r = requests.post(url=URL, data=json_data)
data = r.json()
print(data)