
from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        print("Starting manual migration...")
        try:
            # 1. Add columns to students table
            db.session.execute(text("ALTER TABLE students ADD COLUMN base_total_classes INT DEFAULT 0"))
            db.session.execute(text("ALTER TABLE students ADD COLUMN base_present_days INT DEFAULT 0"))
            db.session.execute(text("ALTER TABLE students ADD COLUMN base_absent_days INT DEFAULT 0"))
            print("Successfully added base columns to 'students' table.")
        except Exception as e:
            print(f"Note: Could not add columns to 'students' (they might already exist): {e}")

        try:
            # 2. Add column to attendance_logs table
            db.session.execute(text("ALTER TABLE attendance_logs ADD COLUMN class_name VARCHAR(20)"))
            print("Successfully added 'class_name' to 'attendance_logs' table.")
        except Exception as e:
            print(f"Note: Could not add 'class_name' to 'attendance_logs': {e}")
        
        db.session.commit()
        print("Migration complete.")

if __name__ == "__main__":
    migrate()
