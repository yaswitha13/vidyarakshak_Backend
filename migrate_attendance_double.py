from app import app, db
from sqlalchemy import text

def alter_attendance_column():
    with app.app_context():
        print("Altering attendance column to DOUBLE (Float)...")
        with db.engine.connect() as conn:
            # Change attendance column in students table
            conn.execute(text("ALTER TABLE students MODIFY COLUMN attendance DOUBLE DEFAULT 100.0"))
            conn.commit()
            print("Migration complete!")

if __name__ == "__main__":
    alter_attendance_column()
