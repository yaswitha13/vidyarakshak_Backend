from app import app, db, Student, AttendanceLog
from sqlalchemy import func, case

def run_test():
    with app.app_context():
        s = Student.query.first()
        if not s:
            print("No students found.")
            return
            
        print(f"Testing for Student: {s.name} (Roll: {s.roll_no}, School: {s.school_code})")
        print(f"Current Student Record: Total={s.total_classes}, Present={s.present_days}, Absent={s.absent_days}, %={s.attendance_percentage}")
        
        stats = db.session.query(
            func.count(AttendanceLog.id),
            func.sum(case((func.upper(AttendanceLog.status) == 'PRESENT', 1), else_=0)),
            func.sum(case((func.upper(AttendanceLog.status) == 'ABSENT', 1), else_=0))
        ).filter(
            AttendanceLog.student_roll_no == s.roll_no,
            AttendanceLog.school_code == s.school_code
        ).first()
        
        print(f"Query Stats Result: {stats}")
        
        total = stats[0] or 0
        present = stats[1] or 0
        absent = stats[2] or 0
        
        if total > 0:
            percentage = (present / total) * 100
        else:
            percentage = 100.0
            
        print(f"Calculated Sync Value: %={percentage}")
        
        if round(percentage, 2) != round(s.attendance_percentage, 2):
            print("MISMATCH DETECTED! Student record is out of sync with logs.")
        else:
            print("Student record is in sync with logs.")

if __name__ == "__main__":
    run_test()
