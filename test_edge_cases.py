import urllib.request
import urllib.error
import json

def test_api(email, role):
    req = urllib.request.Request(
        'http://127.0.0.1:5000/api/forgot-password', 
        data=json.dumps({'email': email, 'role': role}).encode(), 
        headers={'Content-Type': 'application/json'}
    )
    try:
        response = urllib.request.urlopen(req)
        return response.getcode(), response.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()

print("Testing empty email string:")
print(test_api("", "Teacher"))

print("\\nTesting spaces only email string:")
print(test_api("   ", "Teacher"))

print("\\nTesting missing parameter payload (Teacher role, no email):")
req = urllib.request.Request(
    'http://127.0.0.1:5000/api/forgot-password', 
    data=json.dumps({'role': 'Teacher'}).encode(), 
    headers={'Content-Type': 'application/json'}
)
try:
    with urllib.request.urlopen(req) as response:
        print(response.getcode(), response.read().decode())
except urllib.error.HTTPError as e:
    print(e.code, e.read().decode())
