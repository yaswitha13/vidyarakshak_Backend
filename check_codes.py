from app import app, db, Student, AttendanceLog
from sqlalchemy import func

with app.app_context():
    print("Distinct School Codes in Students table:")
    codes = db.session.query(Student.school_code).distinct().all()
    for c in codes:
        print(f" - '{c[0]}'")
        
    print("\nDistinct School Codes in AttendanceLog table:")
    codes = db.session.query(AttendanceLog.school_code).distinct().all()
    for c in codes:
        print(f" - '{c[0]}'")
        
    print("\nExample Student Record:")
    s = Student.query.first()
    if s:
        print(f"Name: {s.name} | Roll: {s.roll_no} | School: {s.school_code}")
