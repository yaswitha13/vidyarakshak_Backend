import pymysql
from config import Config

def create_database():
    # Parse URI: mysql+pymysql://root:@localhost/vidhyarakshak
    # We need to connect without the database name first
    try:
        conn = pymysql.connect(host='localhost', user='root', password='')
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS vidhyarakshak")
        print("Database 'vidhyarakshak' ensured.")
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")

if __name__ == "__main__":
    create_database()
