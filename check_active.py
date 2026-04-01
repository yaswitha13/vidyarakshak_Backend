
from app import app, db, User, Teacher, Student
with app.app_context():
    active_users = User.query.filter_by(status='Active').all()
    print(f"Active Users: {len(active_users)}")
    for u in active_users:
        print(f"User: {u.full_name}, Email: {u.email}, Role: {u.role}")
        
    teachers = Teacher.query.all()
    print(f"\nTotal Teachers: {len(teachers)}")
    for t in teachers:
        print(f"Teacher: {t.name}, Email: {t.email}, Class: {t.class_assigned}, School: {t.school_code}")
    
    students = Student.query.all()
    print(f"\nTotal Students: {len(students)}")
    for s in students:
        print(f"Student: {s.name}, Roll: {s.roll_no}, Class: {s.class_name}, School: {s.school_code}")
