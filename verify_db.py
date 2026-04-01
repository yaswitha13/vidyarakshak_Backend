from app import app, db, User, Student

def verify_db():
    with app.app_context():
        print("--- Users ---")
        users = User.query.all()
        for u in users:
            print(f"Name: {u.full_name}, Email: {u.email}, Role: {u.role}")

        print("\n--- Students ---")
        students = Student.query.all()
        for s in students:
            print(f"Name: {s.name}, Roll: {s.roll_no}, Risk: {s.risk_level}, Attendance: {s.attendance}%")

if __name__ == "__main__":
    verify_db()
