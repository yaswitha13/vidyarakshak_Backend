from app import app, db

def ensure_database_objects():
    with app.app_context():
        print("Ensuring all tables exist (without deleting existing data)...")
        db.create_all()
        print("Database structure is up-to-date and PRESERVED!")

if __name__ == "__main__":
    ensure_database_objects()
