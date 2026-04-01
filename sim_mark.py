
from app import app, db, Student, AttendanceLog
from datetime import datetime

with app.app_context():
    s = Student.query.filter_by(roll_no='101', school_code='102').first()
    if not s:
        print("Ravi not found")
        exit()
        
    print(f"BEFORE: Total={s.total_classes}, Present={s.present_days}, Percent={s.attendance_percentage}")
    
    # Simulate marking ABSENT today
    log_date = datetime.now().strftime('%Y-%m-%d')
    existing = AttendanceLog.query.filter_by(student_roll_no='101', school_code='102', entry_date=log_date).first()
    if existing:
        existing.status = 'ABSENT'
        print(f"Updating existing log for {log_date}")
    else:
        log = AttendanceLog(student_roll_no='101', school_code='102', status='ABSENT', entry_date=log_date)
        db.session.add(log)
        print(f"Added new log for {log_date}")
        
    db.session.flush()
    
    # Call the logic which I'm testing
    from app import calculate_dropout_risk
    calculate_dropout_risk(s)
    
    db.session.commit()
    
    # Re-fetch from DB to check persistence
    db.session.expire_all()
    s2 = Student.query.filter_by(roll_no='101', school_code='102').first()
    print(f"AFTER: Total={s2.total_classes}, Present={s2.present_days}, Percent={s2.attendance_percentage}")
