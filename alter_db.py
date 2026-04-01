import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='vidhyarakshak',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with conn.cursor() as cursor:
        print("Adding school_code column...")
        try:
            cursor.execute("ALTER TABLE students ADD COLUMN school_code VARCHAR(100) DEFAULT 'VDY-102'")
            print("Successfully added school_code.")
        except pymysql.err.OperationalError as e:
            if e.args[0] == 1060: # duplicate column
                print("school_code column already exists, proceeding to update data.")
            else:
                raise e

        # Set any null values
        cursor.execute("UPDATE students SET school_code='VDY-102' WHERE school_code IS NULL OR school_code=''")
        conn.commit()
        print("Updated existing records to VDY-102.")

        # Test user 1001
        cursor.execute("SELECT id, name, roll_no, school_code FROM students WHERE roll_no='1001'")
        print(f"Row 1001 Data: {cursor.fetchone()}")
        
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()
