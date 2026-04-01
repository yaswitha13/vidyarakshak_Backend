import random
from app import app, db, Student

def reseeding_students_fully():
    telugu_names = [
        "Rushithya", "Akhila", "Radha", "Suresh", "Kiran", 
        "Anitha", "Praveen", "Lakshmi", "Teja", "Divya",
        "Venkatesh", "Ramya", "Swathi", "Ganesh", "Mahesh", 
        "Srinivas", "Bhavani", "Karthik", "Sravani", "Harish",
        "Ramesh", "Sujatha", "Rajesh", "Kavitha", "Naveen",
        "Padma", "Satish", "Jyothi", "Manoj", "Sreekanth"
    ]
    
    incomes = ["Under 1 Lakh", "1-2 Lakhs", "2-5 Lakhs", "Above 5 Lakhs"]
    edu_levels = ["Primary", "Secondary", "Higher Secondary", "Graduate", "Illiterate"]
    occupations = ["Farmer", "Daily Wager", "Shop Owner", "Clerk", "Teacher", "Driver"]
    environments = ["Supportive", "Neutral", "Unsupportive", "Stressed"]
    housing = ["Pucca House", "Kutcha House", "Rented", "Own House"]
    migration = ["Low", "Medium", "High"]
    resources = ["Adequate", "Inadequate", "Good", "Poor"]
    involvements = ["High", "Medium", "Low", "None"]
    addresses = ["Gandhi Nagar, Ward 4", "Main Bazaar Road", "Temple Street", "Station Road", "Subhash Nagar", "Village Panchayat limit"]
    
    with app.app_context():
        # Clean up old dummy students generated with 'CLS' or specific exact class names
        strict_dummies = Student.query.all()
        for s in strict_dummies:
            # We ONLY delete if it is one of our Telugu names so we don't accidentally wipe user's real student '1004' named 'sai'
            if s.name in telugu_names:
                db.session.delete(s)
                
        db.session.commit()
        
        added_count = 0
        
        for class_num in range(1, 11):
            class_name = str(class_num)
            
            student_count = random.randint(4, 5)
            
            for i in range(student_count):
                student_name = random.choice(telugu_names)
                
                # Roll no format logic explicitly requested: class 1 -> 101, class 10 -> 1001
                new_roll_int = (class_num * 100) + i + 1
                roll_no = str(new_roll_int)
                
                if Student.query.filter_by(roll_no=roll_no).first():
                    continue
                
                # Random DOB logic
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
                    
                    # Keep counts starting from 0 as explicitly requested
                    total_classes=0,
                    present_days=0,
                    absent_days=0,
                    attendance_percentage=0.0,
                    attendance=0,
                    risk_level="LOW",
                    
                    # Extra metadata adding family income and ALL nullable fields
                    family_income=random.choice(incomes),
                    parents_edu=random.choice(edu_levels),
                    parents_occ=random.choice(occupations),
                    distance=f"{random.randint(1, 15)} km",
                    num_siblings=random.randint(0, 4),
                    home_env=random.choice(environments),
                    housing_cond=random.choice(housing),
                    migration_risk=random.choice(migration),
                    learning_res=random.choice(resources),
                    parent_involv=random.choice(involvements),
                    
                    parent_name=f"{student_name}'s Parent",
                    mobile_number=f"98{random.randint(10000000, 99999999)}",
                    parent_email=f"{student_name.lower()}parent@simats.edu",
                    address=f"H.No {random.randint(1,100)}, {random.choice(addresses)}"
                )
                
                db.session.add(new_student)
                added_count += 1
                
        db.session.commit()
        print(f"Successfully fully re-seeded {added_count} dummy students correctly into the database!")

if __name__ == "__main__":
    reseeding_students_fully()
