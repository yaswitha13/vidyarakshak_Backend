
import urllib.request
import json

base_url = "http://127.0.0.1:5000"

with open('test_results.txt', 'w', encoding='utf-8') as log:
    def check_endpoint(url, desc):
        log.write(f"\n--- {desc} ---\nURL: {url}\n")
        try:
            with urllib.request.urlopen(url) as response:
                log.write(f"Status: {response.getcode()}\n")
                data = response.read().decode('utf-8')
                parsed = json.loads(data)
                log.write(f"Count: {len(parsed) if isinstance(parsed, list) else 1}\n")
                log.write(f"First 200 chars: {data[:200]}\n")
        except Exception as e:
            log.write(f"Error: {e}\n")

    check_endpoint(f"{base_url}/get-teacher-profile?email=paruchuriyaswitha13@gmail.com", "Yaswitha Profile")
    check_endpoint(f"{base_url}/get-students?school_code=102&class_name=2", "Yaswitha Students (Class 2)")
    check_endpoint(f"{base_url}/get-students?school_code=102&class_name=1", "Sai Students (Class 1)")
    check_endpoint(f"{base_url}/get-students?school_code=102", "All School 102 Students")

print("Done")
