
import urllib.request
import json

base_url = "http://127.0.0.1:5000"

def check_endpoint(url):
    print(f"\nTesting: {url}")
    try:
        with urllib.request.urlopen(url) as response:
            print(f"Status: {response.getcode()}")
            data = response.read().decode('utf-8')
            print(f"Response: {data[:500]}...")
    except Exception as e:
        print(f"Error: {e}")

# Check teacher profile for Yaswitha
check_endpoint(f"{base_url}/get-teacher-profile?email=paruchuriyaswitha13@gmail.com")

# Check students for Yaswitha's class (Class 2, School 102)
check_endpoint(f"{base_url}/get-students?school_code=102&class_name=2")

# Check students for sai's class (Class 1, School 102)
# Since students have class "1st", I'll try both "1" (which normalizes to "1st") and "1st" (which also normalizes to "1st").
check_endpoint(f"{base_url}/get-students?school_code=102&class_name=1")

# Check all students for school 102
check_endpoint(f"{base_url}/get-students?school_code=102")
