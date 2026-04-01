from app import db, Student
try:
    with db.app.app_context():
        count = Student.query.count()
        print(f"Connection successful. Student count: {count}")
except Exception as e:
    print(f"Connection failed: {e}")
