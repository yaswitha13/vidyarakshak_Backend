from app import app, db
from sqlalchemy import text

def update_db_schema():
    with app.app_context():
        try:
            # Use raw SQL to add the missing columns
            queries = [
                "ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'Admin' AFTER password",
                "ALTER TABLE users ADD COLUMN school_code VARCHAR(20) DEFAULT '102' AFTER role",
                "ALTER TABLE users ADD COLUMN class_assigned VARCHAR(20) AFTER school_code",
                "ALTER TABLE users ADD COLUMN student_id VARCHAR(50) AFTER class_assigned",
                "ALTER TABLE users MODIFY COLUMN email VARCHAR(120) NULL"
            ]
            
            for query in queries:
                try:
                    db.session.execute(text(query))
                    db.session.commit()
                    print(f"Executed: {query}")
                except Exception as e:
                    print(f"Skipping (likely already exists): {query} - {e}")
            
            print("Database schema update completed!")
        except Exception as e:
            print(f"General Error: {e}")

if __name__ == "__main__":
    update_db_schema()
