from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        # 1. Add gender to teachers
        try:
            db.session.execute(text("ALTER TABLE teachers ADD COLUMN gender VARCHAR(10)"))
            db.session.commit()
            print("Added 'gender' column to 'teachers' table.")
        except Exception as e:
            db.session.rollback()
            print(f"Skipping 'teachers' gender (might already exist): {e}")

        # 2. Add gender to admin_profiles
        try:
            db.session.execute(text("ALTER TABLE admin_profiles ADD COLUMN gender VARCHAR(10)"))
            db.session.commit()
            print("Added 'gender' column to 'admin_profiles' table.")
        except Exception as e:
            db.session.rollback()
            print(f"Skipping 'admin_profiles' gender (might already exist): {e}")

    print("Migration finished!")

if __name__ == "__main__":
    migrate()
