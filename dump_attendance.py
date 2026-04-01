from app import app, db, AttendanceLog, Student
from sqlalchemy import func

with app.app_context():
    print("Last 10 Attendance Logs:")
    logs = AttendanceLog.query.order_by(AttendanceLog.id.desc()).limit(10).all()
    for l in logs:
        print(f"ID: {l.id} | Roll: {l.student_roll_no} | Status: {l.status} | Date: {l.entry_date} | School: {l.school_code}")
    
    print("\nStudent Counts for Roll '101' (example):")
    s = Student.query.filter_by(roll_no='101').first()
    if s:
        print(f"Student: {s.name} | Roll: {s.roll_no} | School: {s.school_code}")
        count = AttendanceLog.query.filter_by(student_roll_no=s.roll_no, school_code=s.school_code).count()
        print(f"Log Count for this student: {count}")
    else:
        print("Student with Roll '101' not found.")
