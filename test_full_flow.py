import urllib.request
import urllib.error
import json
import time

def make_request(url, data):
    req = urllib.request.Request(
        f'http://127.0.0.1:5001{url}', 
        data=json.dumps(data).encode(), 
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode()
    except urllib.error.HTTPError as e:
        print(f"ERROR {e.code}: {e.read().decode()}")
        return None

email = 'teacher@example.com'
role = 'Teacher'

print("1. Requesting forgot password...")
res = make_request('/api/forgot-password', {'email': email, 'role': role})
print("Result:", res)

time.sleep(1) # wait for db

print("2. Fetching OTP from DB using app context...")
from app import app, OTP
with app.app_context():
    otp_record = OTP.query.filter_by(email=email, role=role).order_by(OTP.id.desc()).first()
    if not otp_record:
        print("FAILED: No OTP found in database.")
        exit(1)
    otp_code = otp_record.otp_code

print("Found OTP:", otp_code)

print("3. Verifying OTP...")
res = make_request('/api/verify-otp', {'email': email, 'role': role, 'otp_code': otp_code})
print("Result:", res)

print("4. Resetting password...")
res = make_request('/api/reset-password', {'email': email, 'role': role, 'otp_code': otp_code, 'new_password': 'newpassword123'})
print("Result:", res)

print("5. Attempting login with new password...")
res = make_request('/login', {'email': email, 'password': 'newpassword123', 'role': role})
print("Result:", res)
