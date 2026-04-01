import random
from app import app, db, Student

def seed_dummy_students():
    telugu_names = [
        "Rushithya", "Akhila", "Radha", "Suresh", "Kiran", 
        "Anitha", "Praveen", "Lakshmi", "Teja", "Divya",
        "Venkatesh", "Ramya", "Swathi", "Ganesh", "Mahesh", 
        "Srinivas", "Bhavani", "Karthik", "Sravani", "Harish",
        "Ramesh", "Sujatha", "Rajesh", "Kavitha", "Naveen",
        "Padma", "Satish", "Jyothi", "Manoj", "Sreekanth"
    ]
    
    sections = ["A", "B"]
    
    with app.app_context():
        # Optional: we won't delete all students, just add new ones securely
        # so we don't destroy the user's previously added real students.
        
        added_count = 0
        
        for class_num in range(1, 11):
            class_name = f"Class {class_num}"
            
            # Randomly pick 4 to 5 students for this class
            student_count = random.randint(4, 5)
            
            for i in range(student_count):
                student_name = random.choice(telugu_names)
                # Ensure variation
                if random.random() > 0.5:
                    section = "A"
                else:
                    section = "B"
                    
                full_class_name = f"{class_name} {section}"
                
                # Create a unique roll number
                # format: CLS{class_num}{section}-{i+1}
                roll_no = f"CLS{class_num}{section}-{random.randint(1000, 9999)}"
                
                # Check if roll_no exists just in case
                if Student.query.filter_by(roll_no=roll_no).first():
                    continue
                
                # Mock attendance data
                total_classes = random.randint(150, 200)
                # Randomize attendance percentage between 60% and 98%
                attendance_perc = random.uniform(60.0, 98.0)
                present_days = int((attendance_perc / 100) * total_classes)
                absent_days = total_classes - present_days
                
                # Determine risk level based on attendance (just for realism in testing)
                if attendance_perc < 75.0:
                    risk_level = "HIGH"
                elif attendance_perc < 85.0:
                    risk_level = "MEDIUM"
                else:
                    risk_level = "LOW"
                
                new_student = Student(
                    name=student_name,
                    class_name=full_class_name,
                    roll_no=roll_no,
                    school_code="102",  # Default used in app
                    gender=random.choice(["Male", "Female"]),
                    total_classes=total_classes,
                    present_days=present_days,
                    absent_days=absent_days,
                    attendance_percentage=round(attendance_perc, 1),
                    attendance=round(attendance_perc),
                    risk_level=risk_level,
                    parent_name=f"{student_name}'s Parent",
                    mobile_number=f"98{random.randint(10000000, 99999999)}"
                )
                
                db.session.add(new_student)
                added_count += 1
                
        db.session.commit()
        print(f"Successfully seeded {added_count} dummy students into the database!")

if __name__ == "__main__":
    seed_dummy_students()
