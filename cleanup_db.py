from app import app, db
from sqlalchemy import text

def drop_column_if_exists(table, column):
    try:
        # Check if column exists
        result = db.session.execute(text(f"SHOW COLUMNS FROM {table} LIKE '{column}'"))
        if result.fetchone():
            print(f"Dropping column {column} from {table}...")
            db.session.execute(text(f"ALTER TABLE {table} DROP COLUMN {column}"))
            db.session.commit()
            print(f"Successfully dropped {column} from {table}")
        else:
            print(f"Column {column} does not exist in {table}")
    except Exception as e:
        db.session.rollback()
        print(f"Error dropping {column} from {table}: {e}")

with app.app_context():
    # Columns requested to be removed
    columns_to_drop = [
        'parents_edu',
        'home_env',
        'housing_cond',
        'migration_risk',
        'learning_res',
        'parent_email'
    ]
    
    for col in columns_to_drop:
        drop_column_if_exists('students', col)

print("Cleanup task completed.")
