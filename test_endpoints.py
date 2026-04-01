
import requests
import json

base_url = "http://127.0.0.1:5000"

def check_endpoint(url):
    print(f"\nTesting: {url}")
    try:
        r = requests.get(url)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text[:500]}")
    except Exception as e:
        print(f"Error: {e}")

# Check teacher profile for Yaswitha
check_endpoint(f"{base_url}/get-teacher-profile?email=paruchuriyaswitha13@gmail.com")

# Check students for Yaswitha's class (Class 2, School 102)
check_endpoint(f"{base_url}/get-students?school_code=102&class_name=2")

# Check students for sai's class (Class 1, School 102)
check_endpoint(f"{base_url}/get-students?school_code=102&class_name=1")

# Check all students for school 102
check_endpoint(f"{base_url}/get-students?school_code=102")
