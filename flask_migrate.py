from app import app, db, Student

with app.app_context():
    # If a student exists with school_code null/empty, we default to VDY-102
    students = Student.query.all()
    count = 0
    for s in students:
        if not getattr(s, 'school_code', None):
            s.school_code = 'VDY-102'
            count += 1
    
    if count > 0:
        db.session.commit()
        print(f"Patched {count} older students with VDY-102 school_code.")
    else:
        print("No older students needed patching or school_code already populated.")
        
    for s in Student.query.all():
        print(f"ID: {s.id}, Name: {s.name}, Roll: {s.roll_no}, School: {getattr(s, 'school_code', 'MISSING')}")
