from app import app, db, Student, AttendanceLog

with app.app_context():
    students = Student.query.limit(5).all()
    print("Sample Students:")
    for s in students:
        print(f"Name: {s.name} | Roll: {s.roll_no} | School: '{s.school_code}'")
    
    logs = AttendanceLog.query.limit(5).all()
    print("\nSample Logs:")
    for l in logs:
        print(f"ID: {l.id} | Roll: {l.student_roll_no} | School: '{l.school_code}'")
