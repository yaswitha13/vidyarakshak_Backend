from app import app, Student
with app.app_context():
    for s in Student.query.all():
        print(f"Student: {s.name} | Class: {s.class_name} | School: {s.school_code}")
