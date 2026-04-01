
from app import app, Teacher, Student
with app.app_context():
    sai = Teacher.query.filter_by(email='paruchurisai9@gmail.com').first()
    if sai:
        print(f"Teacher SAI: Name={sai.name}, Class={sai.class_assigned}, School='{sai.school_code}'")
        students = Student.query.filter_by(school_code=sai.school_code).all()
        print(f"Students in school '{sai.school_code}': {len(students)}")
        for s in students:
            print(f" - Student {s.name}: Class={s.class_name}")
    else:
        print("Teacher SAI not found by email paruchurisai9@gmail.com")
