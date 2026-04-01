import random
from app import app, db, Student

def reseeding_students():
    telugu_names = [
        "Rushithya", "Akhila", "Radha", "Suresh", "Kiran", 
        "Anitha", "Praveen", "Lakshmi", "Teja", "Divya",
        "Venkatesh", "Ramya", "Swathi", "Ganesh", "Mahesh", 
        "Srinivas", "Bhavani", "Karthik", "Sravani", "Harish",
        "Ramesh", "Sujatha", "Rajesh", "Kavitha", "Naveen",
        "Padma", "Satish", "Jyothi", "Manoj", "Sreekanth"
    ]
    
    incomes = ["Under 1 Lakh", "1-2 Lakhs", "2-5 Lakhs", "Above 5 Lakhs"]
    
    with app.app_context():
        # Clean up old dummy students generated with 'CLS' or IDs >= 9
        # To be safe, let's delete anything starting with 'CLS'
        old_dummies = Student.query.filter(Student.roll_no.like('CLS%')).all()
        for s in old_dummies:
            db.session.delete(s)
        
        # Also clean up previously generated strict ones if this script is re-run
        strict_dummies = Student.query.filter(Student.roll_no.like('%00%')).all()
        for s in strict_dummies:
            # ONLY delete if it is one of our Telugu names so we don't accidentally wipe user's real student '1004' named 'sai'
            if s.name in telugu_names:
                db.session.delete(s)
                
        db.session.commit()
        
        added_count = 0
        
        for class_num in range(1, 11):
            class_name = str(class_num)
            
            # 4 to 5 students per class
            student_count = random.randint(4, 5)
            
            for i in range(student_count):
                student_name = random.choice(telugu_names)
                
                # Roll no format: class 1 -> 1001, class 2 -> 2001, class 10 -> 10001
                # To do this safely, we will just use (class_num * 1000) + i + 1
                new_roll_int = (class_num * 1000) + i + 1
                roll_no = str(new_roll_int)
                
                # Check if exists
                if Student.query.filter_by(roll_no=roll_no).first():
                    continue
                
                # Random DOB logic
                # Assume students are approx 5 + class_num years old
                # For class 1 -> 6 years old (born ~2020)
                year = 2026 - (5 + class_num)
                month = random.randint(1, 12)
                day = random.randint(1, 28)
                dob_str = f"{day:02d}-{month:02d}-{year}"
                
                new_student = Student(
                    name=student_name,
                    class_name=class_name,
                    roll_no=roll_no,
                    school_code="102",
                    gender=random.choice(["Male", "Female"]),
                    dob=dob_str,
                    
                    # Core Requirements: keep counts starting from 0
                    total_classes=0,
                    present_days=0,
                    absent_days=0,
                    attendance_percentage=0.0,
                    attendance=0,
                    risk_level="LOW",
                    
                    # Extra metadata adding family income
                    family_income=random.choice(incomes),
                    
                    parent_name=f"{student_name}'s Parent",
                    mobile_number=f"98{random.randint(10000000, 99999999)}"
                )
                
                db.session.add(new_student)
                added_count += 1
                
        db.session.commit()
        print(f"Successfully re-seeded {added_count} dummy students correctly into the database!")

if __name__ == "__main__":
    reseeding_students()
