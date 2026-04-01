from app import app, db, Student, AttendanceLog
from sqlalchemy import func, case

def calculate_dropout_risk(s):
    high_factors = 0
    med_factors = 0
    
    # Debugging logs
    print(f"DEBUG: Calculating risk for Student {s.name} (Roll: {s.roll_no}, School: {s.school_code})")
    
    # 1. Robust Attendance Calculation from actual logs
    stats = db.session.query(
        func.count(AttendanceLog.id),
        func.sum(case((func.upper(AttendanceLog.status) == 'PRESENT', 1), else_=0)),
        func.sum(case((func.upper(AttendanceLog.status) == 'ABSENT', 1), else_=0))
    ).filter(
        AttendanceLog.student_roll_no == s.roll_no,
        AttendanceLog.school_code == s.school_code
    ).first()

    total_classes = stats[0] or 0
    present_days = stats[1] or 0
    absent_days = stats[2] or 0
    
    print(f"DEBUG: Found Logs - Total: {total_classes}, Present: {present_days}, Absent: {absent_days}")
    
    # Sync these back to the student record for persistent views
    s.total_classes = total_classes
    s.present_days = present_days
    s.absent_days = absent_days
    
    if total_classes > 0:
        s.attendance_percentage = (present_days / total_classes) * 100
    else:
        s.attendance_percentage = 100.0
    
    print(f"DEBUG: Final Percentage: {s.attendance_percentage}%")
    
    s.attendance = round(s.attendance_percentage) # Sync the integer field with proper rounding
    
    # ... (rest of the risk calculation logic)
    # Priority 1: Attendance Risk Levels requested by user
    attendance_risk = "LOW"
    if s.attendance_percentage < 60.0:
        attendance_risk = "HIGH"
    elif s.attendance_percentage <= 75.0:
        attendance_risk = "MEDIUM"
        
    s.risk_level = attendance_risk
