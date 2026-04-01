from app import app, db
from sqlalchemy import inspect, text

def fix_all_missing_service_columns():
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        # Table -> Missing Column map
        migrations = {
            'attendance_logs': [
                "ALTER TABLE attendance_logs ADD COLUMN school_code VARCHAR(20) DEFAULT '102'"
            ],
            'counseling_records': [
                "ALTER TABLE counseling_records ADD COLUMN school_code VARCHAR(20) DEFAULT '102'"
            ],
            'students': [
                "ALTER TABLE students ADD COLUMN school_code VARCHAR(20) DEFAULT '102'"
            ],
            'users': [
                "ALTER TABLE users ADD COLUMN school_code VARCHAR(20) DEFAULT '102'"
            ]
        }
        
        for table, queries in migrations.items():
            if table in tables:
                columns = [c['name'] for c in inspector.get_columns(table)]
                for query in queries:
                    col_name = query.split('ADD COLUMN ')[1].split(' ')[0]
                    if col_name not in columns:
                        print(f"Fixing {table}: Adding {col_name}...")
                        try:
                            db.session.execute(text(query))
                            db.session.commit()
                            print(f"Successfully added {col_name} to {table}")
                        except Exception as e:
                            print(f"Error adding {col_name} to {table}: {e}")
                            db.session.rollback()
                    else:
                        print(f"Table {table} already has {col_name}")

if __name__ == "__main__":
    fix_all_missing_service_columns()
