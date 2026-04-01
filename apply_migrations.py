from app import app, db
from sqlalchemy import text

def add_column_if_not_exists(table, column, definition):
    try:
        # Check if column exists
        result = db.session.execute(text(f"SHOW COLUMNS FROM {table} LIKE '{column}'"))
        if not result.fetchone():
            print(f"Adding column {column} to {table}...")
            db.session.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {definition}"))
            db.session.commit()
            print(f"Successfully added {column} to {table}")
        else:
            print(f"Column {column} already exists in {table}")
    except Exception as e:
        db.session.rollback()
        print(f"Error adding {column} to {table}: {e}")

with app.app_context():
    # Teachers table additions
    add_column_if_not_exists('teachers', 'status', "VARCHAR(20) DEFAULT 'PENDING'")
    
    # Students table additions (Attendance Base Stats)
    add_column_if_not_exists('students', 'base_total_classes', "INT DEFAULT 0")
    add_column_if_not_exists('students', 'base_present_days', "INT DEFAULT 0")
    add_column_if_not_exists('students', 'base_absent_days', "INT DEFAULT 0")
    
    # Students table additions (Risk/Ecosystem Factors)
    add_column_if_not_exists('students', 'parents_edu', "VARCHAR(100)")
    add_column_if_not_exists('students', 'parents_occ', "VARCHAR(100)")
    add_column_if_not_exists('students', 'distance', "VARCHAR(50)")
    add_column_if_not_exists('students', 'num_siblings', "INT DEFAULT 0")
    add_column_if_not_exists('students', 'home_env', "VARCHAR(100)")
    add_column_if_not_exists('students', 'housing_cond', "VARCHAR(100)")
    add_column_if_not_exists('students', 'migration_risk', "VARCHAR(100)")
    add_column_if_not_exists('students', 'learning_res', "VARCHAR(100)")
    add_column_if_not_exists('students', 'parent_involv', "VARCHAR(100)")
    add_column_if_not_exists('students', 'parent_email', "VARCHAR(120)")
    
    # Users table additions
    add_column_if_not_exists('users', 'status', "VARCHAR(20) DEFAULT 'Active'")

    # Ensure any completely new tables (like 'alerts') are created
    try:
        db.create_all()
        print("db.create_all() executed for any new tables.")
    except Exception as e:
        print(f"Error in create_all: {e}")

print("Migration task completed.")
