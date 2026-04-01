from app import app, db, User, Teacher, Student, AttendanceLog, calculate_dropout_risk
from datetime import datetime

def seed_data():
    with app.app_context():
        print("Seeding Users...")
        # Admin
        if not User.query.filter_by(email="admin@example.com").first():
            admin = User(
                full_name="System Admin",
                email="admin@example.com",
                password="admin",
                role="Admin",
                school_code="SCH123"
            )
            db.session.add(admin)
        
        # Teacher
        if not Teacher.query.filter_by(email="teacher@example.com").first():
            teacher = Teacher(
                name="John Doe",
                email="teacher@example.com",
                password="teacher",
                school_code="SCH123",
                class_assigned="10th",
                subject="Mathematics",
                phone="9876543210",
                status="APPROVED"
            )
            db.session.add(teacher)

        print("Seeding Students...")
        students_data = [
            {
                "name": "Alice Smith",
                "class_name": "10th",
                "roll_no": "1001",
                "gender": "Female",
                "dob": "2008-05-15",
                "family_income": "High (Above 5L)",
                "total_classes": 100,
                "present_days": 95,
                "absent_days": 5,
                "parent_name": "Robert Smith",
                "mobile_number": "9876543210"
            },
            {
                "name": "Bob Johnson",
                "class_name": "10th",
                "roll_no": "1002",
                "gender": "Male",
                "dob": "2008-08-20",
                "family_income": "Below 50,000",
                "total_classes": 100,
                "present_days": 60,
                "absent_days": 40,
                "parent_name": "Mary Johnson",
                "mobile_number": "9876543211",
                "distance": "> 5 km"
            },
            {
                "name": "Charlie Brown",
                "class_name": "10th",
                "roll_no": "1003",
                "gender": "Male",
                "dob": "2008-12-10",
                "family_income": "50,000 - 1.5L",
                "total_classes": 100,
                "present_days": 80,
                "absent_days": 20,
                "parent_name": "James Brown",
                "mobile_number": "9876543212"
            }
        ]

        for s_data in students_data:
            if not Student.query.filter_by(roll_no=s_data['roll_no']).first():
                student = Student(**s_data)
                calculate_dropout_risk(student)
                db.session.add(student)
        
        db.session.commit()
        print("Database Seeded Successfully!")

if __name__ == "__main__":
    seed_data()
