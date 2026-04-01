from app import app, db, Student

with app.app_context():
    print(f"102 count: {Student.query.filter_by(school_code='102').count()}")
    print(f"VDY-102 count: {Student.query.filter_by(school_code='VDY-102').count()}")
    
    # Check for the students in the screenshot
    for name in ["ravi", "Sravani", "Vennela"]:
        s = Student.query.filter(Student.name.like(f"%{name}%")).first()
        if s:
            print(f"Found {name}: Roll={s.roll_no}, School='{s.school_code}', Class='{s.class_name}'")
        else:
            print(f"NOT Found {name}")
