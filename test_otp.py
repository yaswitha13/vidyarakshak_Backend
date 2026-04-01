import urllib.request
import urllib.error
import json

req = urllib.request.Request(
    'http://127.0.0.1:5001/api/forgot-password', 
    data=json.dumps({'email': 'teacher@example.com', 'role': 'Teacher'}).encode(), 
    headers={'Content-Type': 'application/json'}
)
try:
    with urllib.request.urlopen(req) as response:
        print("SUCCESS:", response.read().decode())
except urllib.error.HTTPError as e:
    print("ERROR:", e.code, e.read().decode())
