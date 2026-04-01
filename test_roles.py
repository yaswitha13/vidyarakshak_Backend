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

print("1. Teacher email acting as Admin:")
print(test_api("teacher@example.com", "Admin"))

print("\\n2. Admin email acting as Teacher:")
print(test_api("paruchuriyaswitha13@gmail.com", "Teacher"))

# Let's also verify that there aren't duplicate users with NULL emails
from app import app, db, User, Teacher
with app.app_context():
    print("\\nUsers with empty emails:", User.query.filter(User.email.in_(['', None])).count())
    print("Teachers with empty emails:", Teacher.query.filter(Teacher.email.in_(['', None])).count())
