
from app import app, db, Teacher, Student
with app.app_context():
    teachers = Teacher.query.all()
    print(f"Total Teachers: {len(teachers)}")
    for t in teachers:
        print(f"Teacher: {t.name}, Email: {t.email}, Class: {t.class_assigned}, School: {t.school_code}")
    
    students = Student.query.all()
    print(f"Total Students: {len(students)}")
    for s in students:
        print(f"Student: {s.name}, Roll: {s.roll_no}, Class: {s.class_name}, School: {s.school_code}")
