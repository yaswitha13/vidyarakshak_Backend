import urllib.request
import urllib.error
import json

def make_request(url, data):
    req = urllib.request.Request(
        f'http://127.0.0.1:5000{url}', 
        data=json.dumps(data).encode(), 
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            return response.getcode(), response.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()

email = 'incorrect_email@example.com'
role = 'Teacher'

print("1. Requesting forgot password with incorrect email...")
code, res = make_request('/api/forgot-password', {'email': email, 'role': role})
print(f"Status Code: {code}")
print("Result:", res)

email2 = 'admin_incorrect@example.com'
role2 = 'Admin'
print("\\n2. Requesting forgot password with incorrect admin email...")
code2, res2 = make_request('/api/forgot-password', {'email': email2, 'role': role2})
print(f"Status Code: {code2}")
print("Result:", res2)
