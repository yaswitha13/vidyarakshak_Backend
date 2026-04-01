
import sys
from app import app, db, User, Teacher, Student

with app.app_context():
    with open('active_users.txt', 'w', encoding='utf-8') as f:
        active_users = User.query.filter_by(status='Active').all()
        f.write(f"Active Users: {len(active_users)}\n")
        for u in active_users:
            f.write(f"User: {u.full_name}, Email: {u.email}, Role: {u.role}\n")
            
        teachers = Teacher.query.all()
        f.write(f"\nTotal Teachers: {len(teachers)}\n")
        for t in teachers:
            f.write(f"Teacher: {t.name}, Email: {t.email}, Class: {t.class_assigned}, School: {t.school_code}\n")
        
        students = Student.query.all()
        f.write(f"\nTotal Students: {len(students)}\n")
        for s in students:
            f.write(f"Student: {s.name}, Roll: {s.roll_no}, Class: {s.class_name}, School: {s.school_code}\n")
print("Report generated in active_users.txt")
