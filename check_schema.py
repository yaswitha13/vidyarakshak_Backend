from app import app, db, Teacher, AdminProfile
from sqlalchemy import inspect

with app.app_context():
    inspector = inspect(db.engine)
    
    for table_name in ['teachers', 'admin_profiles', 'teacher_edit_profile']:
        if table_name in inspector.get_table_names():
            columns = [c['name'] for c in inspector.get_columns(table_name)]
            print(f"Table: {table_name}, Columns: {columns}")
        else:
            print(f"Table: {table_name} NOT FOUND")
