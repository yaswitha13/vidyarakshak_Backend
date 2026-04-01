from app import app, db, Student, AttendanceLog

with app.app_context():
    s = Student.query.filter_by(roll_no='101', school_code='102').first()
    if s:
        log_count = AttendanceLog.query.filter_by(student_roll_no=s.roll_no, school_code=s.school_code).count()
        print(f"Student {s.name}: Record.total={s.total_classes}, Actual.logs={log_count}")
        print(f"Record.pct={s.attendance_percentage}")
