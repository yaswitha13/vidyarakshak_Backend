import sqlite3

try:
    conn = sqlite3.connect('instance/vidhyarakshak.db')
    cursor = conn.cursor()
    # Check if the column exists
    cursor.execute("PRAGMA table_info(students)")
    columns = [info[1] for info in cursor.fetchall()]
    
    if 'school_code' not in columns:
        print("Adding school_code column to students table...")
        cursor.execute("ALTER TABLE students ADD COLUMN school_code VARCHAR(20) DEFAULT '102'")
        
        # Retroactively update old default records like 1001 with 102
        cursor.execute("UPDATE students SET school_code = '102' WHERE school_code IS NULL")
        conn.commit()
        print("Migration complete!")
    else:
        # Just in case some are null
        cursor.execute("UPDATE students SET school_code = '102' WHERE school_code IS NULL")
        conn.commit()
        print("Column already exists. Nulls patched if any existed.")
        
    # Print out students to verify 1001
    cursor.execute("SELECT id, name, roll_no, school_code FROM students")
    print("CURRENT STUDENTS:")
    for row in cursor.fetchall():
        print(row)
        
    conn.close()
except Exception as e:
    print(f"Error: {e}")
