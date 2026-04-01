import pymysql

try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='vidhyarakshak',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    with conn.cursor() as cursor:
        # Check current data
        cursor.execute("SELECT id, name, roll_no, school_code FROM students WHERE roll_no='1001'")
        student_1001 = cursor.fetchone()
        print(f"Before sync: {student_1001}")
        
        # Update null or empty school codes with the default VDY-102 so they match ParentLogin
        cursor.execute("UPDATE students SET school_code = 'VDY-102' WHERE school_code IS NULL OR school_code = ''")
        conn.commit()
        
        # Verify sync
        cursor.execute("SELECT id, name, roll_no, school_code FROM students WHERE roll_no='1001'")
        student_1001 = cursor.fetchone()
        print(f"After sync: {student_1001}")
        
except Exception as e:
    print(f"Database error: {e}")
finally:
    if 'conn' in locals() and conn.open:
        conn.close()
