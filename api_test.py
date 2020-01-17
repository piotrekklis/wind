import requests
import json

r = requests.get('http://localhost:8000/observations/')
r = json.loads(r.text)

print(len(r['results']))
