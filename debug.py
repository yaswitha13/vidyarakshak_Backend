import pymysql

def check_db():
    with open('output.txt', 'w') as f:
        try:
            conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='vidhyarakshak')
            cur = conn.cursor()
            cur.execute("SELECT email, password, status, school_code, class_assigned FROM teachers WHERE email='paruchurisai9@gmail.com'")
            f.write("TEACHERS TABLE: " + str(cur.fetchall()) + "\n")
            
            cur.execute("SELECT email, password, role FROM users WHERE email='paruchurisai9@gmail.com'")
            f.write("USERS TABLE: " + str(cur.fetchall()) + "\n")
            conn.close()
        except Exception as e:
            f.write("Error connecting to MySQL: " + str(e) + "\n")

if __name__ == '__main__':
    check_db()
