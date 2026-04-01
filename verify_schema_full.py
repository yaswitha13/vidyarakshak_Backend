from app import app, db
from sqlalchemy import inspect

with app.app_context():
    inspector = inspect(db.engine)
    print("Checking database tables for 'school_code' column:")
    for table_name in inspector.get_table_names():
        columns = [c['name'] for c in inspector.get_columns(table_name)]
        has_school_code = 'school_code' in columns
        print(f"Table: {table_name:20} | Columns: {columns[:3]}... | school_code: {has_school_code}")
