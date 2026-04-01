from app import app, db, AttendanceLog
from datetime import datetime

with app.app_context():
    today = "26/03/2026"
    print(f"Checking updates for {today}:")
    logs = AttendanceLog.query.filter_by(entry_date=today).all()
    if not logs:
        print("No logs found for today.")
    else:
        for l in logs:
            print(f"Roll: {l.student_roll_no} | Status: {l.status} | Reason: {l.reason}")
