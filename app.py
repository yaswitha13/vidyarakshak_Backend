from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, func, case, text
import os
import smtplib
import random
import threading
from email.mime.text import MIMEText
from config import Config

# Change app initialization to find templates and static files in the website folder
# Since app.py is in backend/, we go up one level to VidhyaRakshak/ and then to website/
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'website'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'website'))

app = Flask(__name__, 
            template_folder=template_dir,
            static_folder=static_dir,
            static_url_path='')
CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)

from datetime import datetime, timedelta

# User Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True) # Optional for some roles
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='Admin') # Admin, Teacher, Parent
    school_code = db.Column(db.String(20), nullable=True)
    class_assigned = db.Column(db.String(20), nullable=True) # For Teachers
    roll_no = db.Column(db.String(50), nullable=True) # For Parents
    login_time = db.Column(db.String(50), nullable=True) # For Activity Tracking
    status = db.Column(db.String(20), nullable=True, default='Active') # For Login Tracking
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.full_name} ({self.role})>'

# Teacher Model (Separate table as requested)
class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.String(50), nullable=True) # Added explicit ID for teachers
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True) # Set during approval
    password = db.Column(db.String(200), nullable=True)        # Set during approval
    subject = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    gender = db.Column(db.String(10)) # Male, Female
    class_assigned = db.Column(db.String(20))
    status = db.Column(db.String(20), default='APPROVED') # Default to APPROVED as requested
    school_code = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Teacher {self.name} ({self.status})>'
#Rendors

# Admin Profile Model
class AdminProfile(db.Model):
    __tablename__ = 'admin_profiles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    gender = db.Column(db.String(10)) # Male, Female
    role = db.Column(db.String(50), default='Administrator')
    school = db.Column(db.String(100))
    state = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<AdminProfile {self.name}>'

# Removed TeacherProfile model to prevent unmigrated DB connection crashes

# Student Model
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(20), nullable=False)
    roll_no = db.Column(db.String(20), nullable=False)
    school_code = db.Column(db.String(20), nullable=False) # Added school_code
    gender = db.Column(db.String(10))
    dob = db.Column(db.String(20))
    
    # Risk Related Fields (Running Totals)
    total_classes = db.Column(db.Integer, default=0)
    present_days = db.Column(db.Integer, default=0)
    absent_days = db.Column(db.Integer, default=0)
    
    # Base Stats (to preserve initial data when logs are empty)
    base_total_classes = db.Column(db.Integer, default=0)
    base_present_days = db.Column(db.Integer, default=0)
    base_absent_days = db.Column(db.Integer, default=0)
    
    attendance_percentage = db.Column(db.Float, default=100.0)
    attendance = db.Column(db.Float, default=100.0) # Updated to Double precision as requested
    risk_level = db.Column(db.String(10), default='LOW') # LOW, MEDIUM, HIGH
    
    # Ecosystem Factors
    family_income = db.Column(db.String(100))
    parents_occ = db.Column(db.String(100))
    distance = db.Column(db.String(50))
    num_siblings = db.Column(db.Integer, default=0)
    parent_involv = db.Column(db.String(100))
    
    parent_name = db.Column(db.String(100))
    mobile_number = db.Column(db.String(20))
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Alert Model (New)
class Alert(db.Model):
    __tablename__ = 'alerts'
    alert_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=True)
    student_name = db.Column(db.String(100), nullable=True)
    roll_number = db.Column(db.String(20), nullable=True)
    attendance = db.Column(db.Integer, nullable=True)
    class_name = db.Column(db.String(20), nullable=True)
    teacher_id = db.Column(db.Integer, nullable=True)
    teacher_name = db.Column(db.String(100), nullable=True)
    alert_type = db.Column(db.String(50), nullable=False)
    alert_message = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), nullable=False) # Low / Medium / High
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Not Seen') # Seen / Not Seen

@event.listens_for(Alert, 'before_insert')
def receive_before_insert(mapper, connection, target):
    # Automatically fetch roll_number and attendance from students table
    if target.student_id:
        from sqlalchemy.orm import object_session
        session = object_session(target)
        if not session:
            # If not yet added to a session, we can query directly
            student = db.session.get(Student, target.student_id)
        else:
            student = session.get(Student, target.student_id)
            
        if student:
            if not target.roll_number:
                target.roll_number = student.roll_no
            if target.attendance is None:
                target.attendance = student.attendance
            if not target.class_name:
                target.class_name = student.class_name

    # Automatically fetch teacher_id from teachers table using class_name
    if target.class_name and not target.teacher_id:
        from sqlalchemy.orm import object_session
        session = object_session(target)
        if not session:
            teacher = Teacher.query.filter_by(class_assigned=target.class_name).first()
        else:
            teacher = session.query(Teacher).filter_by(class_assigned=target.class_name).first()
            
        if teacher:
            target.teacher_id = teacher.id

# Counseling/Behavior Record Model
class CounselingRecord(db.Model):
    __tablename__ = 'counseling_records'
    id = db.Column(db.Integer, primary_key=True)
    student_roll_no = db.Column(db.String(20), nullable=False)
    student_name = db.Column(db.String(100))
    class_name = db.Column(db.String(20))
    counselor_name = db.Column(db.String(100))
    session_date = db.Column(db.String(20))
    counseling_type = db.Column(db.String(100))
    dropout_reason = db.Column(db.String(100))
    student_mood = db.Column(db.String(100))
    progress_status = db.Column(db.String(100))
    behavior_observation = db.Column(db.String(100))
    parent_involvement = db.Column(db.String(100))
    school_code = db.Column(db.String(20), nullable=True) # Added for Strict Matching
    notes = db.Column(db.Text)
    action_plan = db.Column(db.Text)
    followup_date = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Risk History Model
class RiskHistory(db.Model):
    __tablename__ = 'risk_history'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)
    date_recorded = db.Column(db.DateTime, default=datetime.utcnow)

# Attendance Log Model
class AttendanceLog(db.Model):
    __tablename__ = 'attendance_logs'
    id = db.Column(db.Integer, primary_key=True)
    student_roll_no = db.Column(db.String(20), nullable=False)
    school_code = db.Column(db.String(20), nullable=True)
    class_name = db.Column(db.String(20), nullable=True) 
    status = db.Column(db.String(10), nullable=False) # PRESENT, ABSENT
    session_id = db.Column(db.Integer, nullable=False) # Changed to Integer as requested
    reason = db.Column(db.String(200)) # Medical, Family, etc.
    entry_date = db.Column(db.String(20)) # dd/mm/yyyy
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# OTP Model for Forgot Password
class OTP(db.Model):
    __tablename__ = 'otps'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_valid(self):
        return datetime.utcnow() <= self.expires_at

# Create the database tables
with app.app_context():
    db.create_all()

# --- PAGE RENDERS ---
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about_app')
def about_app():
    return render_template('about_app.html')

@app.route('/about_project')
def about_project():
    return render_template('about_project.html')

@app.route('/admin_about_app')
def admin_about_app():
    return render_template('admin_about_app.html')

@app.route('/admin_alerts')
def admin_alerts():
    return render_template('admin_alerts.html')

@app.route('/admin_change_password')
def admin_change_password():
    return render_template('admin_change_password.html')

@app.route('/admin_counseling')
def admin_counseling():
    return render_template('admin_counseling.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/admin_edit_profile')
def admin_edit_profile():
    return render_template('admin_edit_profile.html')

@app.route('/admin_privacy_policy')
def admin_privacy_policy():
    return render_template('admin_privacy_policy.html')

@app.route('/admin_profile')
def admin_profile():
    return render_template('admin_profile.html')

@app.route('/admin_students')
def admin_students():
    return render_template('admin_students.html')

@app.route('/admin_teachers')
def admin_teachers():
    return render_template('admin_teachers.html')

@app.route('/forgot_password', methods=['GET'])
def forgot_password_page():
    return render_template('forgot_password.html')

@app.route('/login_admin')
def login_admin():
    return render_template('login_admin.html')

@app.route('/login_parent')
def login_parent():
    return render_template('login_parent.html')

@app.route('/login_teacher')
def login_teacher():
    return render_template('login_teacher.html')

@app.route('/new_password')
def new_password():
    return render_template('new_password.html')

@app.route('/parent_alerts')
def parent_alerts():
    return render_template('parent_alerts.html')

@app.route('/parent_counseling')
def parent_counseling():
    return render_template('parent_counseling.html')

@app.route('/parent_dashboard')
def parent_dashboard():
    return render_template('parent_dashboard.html')

@app.route('/parent_profile')
def parent_profile():
    return render_template('parent_profile.html')

@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')

@app.route('/support_desk')
def support_desk():
    return render_template('support_desk.html')

@app.route('/teacher_add_student')
def teacher_add_student():
    return render_template('teacher_add_student.html')

@app.route('/teacher_airisk')
def teacher_airisk():
    return render_template('teacher_airisk.html')

@app.route('/teacher_alerts')
def teacher_alerts():
    return render_template('teacher_alerts.html')

@app.route('/teacher_attendance')
def teacher_attendance():
    return render_template('teacher_attendance.html')

@app.route('/teacher_counseling')
def teacher_counseling():
    return render_template('teacher_counseling.html')

@app.route('/teacher_dashboard')
def teacher_dashboard():
    return render_template('teacher_dashboard.html')

@app.route('/teacher_profile')
def teacher_profile():
    return render_template('teacher_profile.html')

@app.route('/teacher_students')
def teacher_students():
    return render_template('teacher_students.html')

@app.route('/verify_otp', methods=['GET'])
def verify_otp_page():
    return render_template('verify_otp.html')

def send_otp_email_thread(to_email, otp_code, app_instance):
    with app_instance.app_context():
        sender_email = app_instance.config.get('SMTP_USER')
        sender_password = app_instance.config.get('SMTP_APP_PASSWORD')
        host = app_instance.config.get('SMTP_HOST')
        port = app_instance.config.get('SMTP_PORT')
        
        msg = MIMEText(f"Your OTP for password reset is: {otp_code}\n\nThis OTP is valid for 10 minutes.")
        msg['Subject'] = 'Password Reset OTP - VidhyaRakshak'
        msg['From'] = sender_email
        msg['To'] = to_email

        try:
            server = smtplib.SMTP(host, port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            server.quit()
            print(f"OTP successfully sent to {to_email}")
        except Exception as e:
            print(f"\n[DEV MOCK] SMTP failed: {e}\n[DEV MOCK] Mocking email send.\n[DEV MOCK] To: {to_email}\n[DEV MOCK] OTP: {otp_code}\n")

def send_otp_email(to_email, otp_code):
    # Dispatch email sending to a background thread to avoid blocking the main request thread
    thread = threading.Thread(target=send_otp_email_thread, args=(to_email, otp_code, app))
    thread.start()
    return True # Always return true to allow request to proceed immediately

import re
def normalize_class(raw):
    if not raw: return ""
    raw_str = str(raw).strip().lower()
    # Remove "class" prefix if present
    cleaned = re.sub(r'(?i)^class\s+', '', raw_str).strip()
    
    if cleaned.isdigit():
        num = int(cleaned)
        if 11 <= (num % 100) <= 13:
            suffix = "th"
        elif num % 10 == 1:
            suffix = "st"
        elif num % 10 == 2:
            suffix = "nd"
        elif num % 10 == 3:
            suffix = "rd"
        else:
            suffix = "th"
        cleaned = f"{num}{suffix}"
    return cleaned

def normalize_date(raw_date):
    """
    Standardize incoming dates into strictly 'yyyy-mm-dd' internally?
    Wait no, current DB expects 'dd/mm/yyyy'.
    Falls back to today's date in dd/mm/yyyy if unparseable.
    """
    if not raw_date or raw_date == "Select Date":
        return datetime.utcnow().strftime("%d/%m/%Y")
    raw_date = str(raw_date).strip()
    
    # Check if format is yyyy-mm-dd
    if "-" in raw_date:
        try:
            date_obj = datetime.strptime(raw_date.split("T")[0], "%Y-%m-%d")
            return date_obj.strftime("%d/%m/%Y")
        except:
            pass
            
    # Format padding for d/m/yyyy or dd/mm/yyyy
    if "/" in raw_date:
        try:
            parts = raw_date.split("/")
            if len(parts) == 3:
                day = int(parts[0])
                month = int(parts[1])
                year = int(parts[2])
                return f"{day:02d}/{month:02d}/{year}"
        except:
            pass
        
    return datetime.utcnow().strftime("%d/%m/%Y")

def normalize_status(st):
    """Normalize P/A status to full PRESENT/ABSENT words for consistency."""
    if not st: return 'PRESENT'
    st = str(st).strip().upper()
    if st in ['P', 'PRESENT']: return 'PRESENT'
    if st in ['A', 'ABSENT']: return 'ABSENT'
    return st

def normalize_session_id(raw):
    """
    If raw is None, empty, or not a positive integer string, return None. 
    Otherwise return integer.
    """
    if raw is None: return None
    raw_str = str(raw).strip()
    if not raw_str or raw_str.lower() == 'default': return None
    
    try:
        val = int(raw_str)
        return val if val > 0 else None
    except:
        return None

def get_next_session_id(student_roll_no, school_code, entry_date, class_name=None):
    """
    Finds the max session_id for this student on this date and returns max + 1.
    If no records exist, returns 1.
    """
    query = db.session.query(func.max(AttendanceLog.session_id)).filter(
        func.trim(AttendanceLog.student_roll_no) == str(student_roll_no).strip(),
        func.trim(AttendanceLog.school_code) == str(school_code).strip(),
        AttendanceLog.entry_date == entry_date
    )
    if class_name:
        query = query.filter(func.trim(AttendanceLog.class_name) == class_name.strip())
        
    max_sid = query.scalar()
    return (max_sid + 1) if max_sid is not None else 1

def calculate_dropout_risk(s):
    high_factors = 0
    med_factors = 0
    # 1. Attendance Calculation strictly from logs as requested
    try:
        s_roll = str(s.roll_no).strip() if s.roll_no else ""
        s_school = str(s.school_code).strip() if s.school_code else ""
        
        if not s_roll:
             total_classes = s.total_classes or 0
             present_days = s.present_days or 0
             absent_days = s.absent_days or 0
        else:
            # Multi-session Calculation: Sum up all sessions recorded
            query = AttendanceLog.query.filter(
                func.trim(AttendanceLog.student_roll_no) == s_roll,
                func.trim(AttendanceLog.school_code) == s_school
            )
            # Strict Filtering if class name is specified
            if s.class_name:
                query = query.filter(func.trim(AttendanceLog.class_name) == s.class_name.strip())
                
            stats = db.session.query(
                func.count(AttendanceLog.id), # Total Sessions
                func.sum(case((func.trim(func.upper(AttendanceLog.status)).in_(['PRESENT', 'P']), 1), else_=0)), # Present Sessions
                func.sum(case((func.trim(func.upper(AttendanceLog.status)).in_(['ABSENT', 'A']), 1), else_=0))   # Absent Sessions
            ).filter(
                AttendanceLog.id.in_(query.with_entities(AttendanceLog.id))
            ).first()

            # The source of truth is the session counts
            total_sessions = int(stats[0]) if stats[0] is not None else 0
            present_sessions = int(stats[1]) if stats[1] is not None else 0
            absent_sessions = int(stats[2]) if stats[2] is not None else 0
            
            # Final Calculation Logic: Base + Sessions
            total_classes = int(s.base_total_classes or 0) + total_sessions
            present_days = int(s.base_present_days or 0) + present_sessions
            absent_days = int(s.base_absent_days or 0) + absent_sessions
            
            # Fallback for empty students
            if total_classes == 0:
                total_classes = int(s.total_classes or 0)
                present_days = int(s.present_days or 0)
                absent_days = int(s.absent_days or 0)
    except Exception as e:
        print(f"Error calculating session-wise attendance: {e}")
        total_classes = int(s.total_classes or 0)
        present_days = int(s.present_days or 0)
        absent_days = int(s.absent_days or 0)

    # Sync these back to the student record
    s.total_classes = total_classes
    s.present_days = present_days
    s.absent_days = absent_days
    
    if total_classes > 0:
        s.attendance_percentage = round((float(present_days) / float(total_classes)) * 100, 2)
    else:
        # Default for new students with no classes yet
        s.attendance_percentage = 100.0
    
    s.attendance = s.attendance_percentage
    db.session.add(s) # Explicitly mark student as dirty for session tracking
    
    # Audit log to verify recalculation is firing
    try:
        with open("attendance_sync.log", "a") as f:
            f.write(f"[{datetime.now()}] SYNC: Student {s.name} ({s.roll_no}) | Total:{s.total_classes} Pres:{s.present_days} New%:{s.attendance_percentage}\n")
    except:
        pass
    
    # Determine base risk purely from attendance as requested
    attendance_risk = "LOW"
    if s.attendance_percentage < 60.0:
        attendance_risk = "HIGH"
        high_factors += 1
    elif s.attendance_percentage <= 75.0:
        attendance_risk = "MEDIUM"
        med_factors += 1

    # 2. Family Income
    income = (s.family_income or "").lower()
    if "below" in income or "50,000" in income and "below" in income: high_factors += 1
    elif "1.5L" in income or "50,000" in income: med_factors += 1

    # 3. Distance
    dist = (s.distance or "").lower()
    if "5" in dist and "more" in dist or "> 5" in dist: high_factors += 1
    elif "2" in dist or "5" in dist: med_factors += 1

    # 5. Parents Occupation
    occ = (s.parents_occ or "").lower()
    if "labor" in occ or "seasonal" in occ: high_factors += 1
    elif "small business" in occ: med_factors += 1

    # 6. Siblings
    num_siblings = s.num_siblings or 0
    if num_siblings >= 3: high_factors += 1
    elif num_siblings >= 1: med_factors += 1

    # 11. Parent Involvement
    inv = (s.parent_involv or "").lower()
    if "never" in inv: high_factors += 1
    elif "sometimes" in inv: med_factors += 1

    # 11. Parent Involvement
    inv = (s.parent_involv or "").lower()
    if "never" in inv: high_factors += 1
    elif "sometimes" in inv: med_factors += 1

    # FINAL CALCULATION
    old_risk = s.risk_level
    
    # Priority 1: Attendance Risk Levels requested by user
    # Priority 2: Multi-factor threshold (4 factors)
    if attendance_risk == "HIGH" or high_factors >= 4:
        s.risk_level = "HIGH"
    elif attendance_risk == "MEDIUM" or med_factors >= 4:
        s.risk_level = "MEDIUM"
    else:
        s.risk_level = "LOW"

    # Save to RiskHistory if changed or new
    if old_risk != s.risk_level:
        # We need s.id to be populated. If it's a new student, id might be None until flush.
        # This will be handled by flushing in the route before calling calculate_dropout_risk.
        if s.id:
            history_entry = RiskHistory(student_id=s.id, risk_level=s.risk_level)
            db.session.add(history_entry)

@app.route('/api/parent/register', methods=['POST'])
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    
    # Auto-detect role if missing based on URL
    role_default = 'Parent' if 'parent' in request.path.lower() else 'Admin'
    role = str(data.get('role') or role_default).strip().title()
    if role == 'Administrator':
        role = 'Admin'
    
    if role == 'Admin':
        return jsonify({"message": "Admin registration is restricted. Please contact system administrator."}), 403
        
    school_code = str(data.get('school_code') or '').strip()
    if not school_code:
        return jsonify({"message": "School Code is required for registration"}), 400
        
    class_assigned = data.get('class_assigned')
    roll_no = str(data.get('roll_no') or data.get('roll_number') or '').strip()

    # Role-based validation
    if role == 'Parent':
        if not all([roll_no, password, confirm_password]):
            return jsonify({"message": "Please enter all required details"}), 400
        
        # Auto-fetch student name as full_name for parents
        student = Student.query.filter_by(roll_no=roll_no, school_code=school_code).first()
        if not student:
            return jsonify({"message": "Student not found with this roll number."}), 404
        full_name = student.name
    else:
        if not all([full_name, password, confirm_password]):
            return jsonify({"message": "Please enter all required details"}), 400

    if password != confirm_password:
        return jsonify({"message": "Passwords do not match"}), 400

    if email and User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    if role == 'Parent' and roll_no:
        if User.query.filter_by(roll_no=roll_no, school_code=school_code, role='Parent').first():
            return jsonify({"message": "roll_no already exists"}), 400

    try:
        if role == 'Teacher':
            teacher = Teacher.query.filter_by(email=email).first()
            if not teacher:
                return jsonify({"message": "Teacher not registered. Admin must add you first."}), 400
            
            if teacher.status == 'PENDING':
                return jsonify({"message": "Teacher approval is still pending."}), 400
            elif teacher.status == 'REJECTED':
                return jsonify({"message": "Teacher registration was rejected."}), 400
            
            # Status is APPROVED. We attach the login credentials securely here.
            teacher.password = password
            db.session.commit()
            return jsonify({"message": "Teacher account created successfully!"}), 201
            
        else:
            new_user = User(
                full_name=full_name,
                email=email,
                password=password,
                role=role,
                school_code=school_code,
                class_assigned=class_assigned,
                roll_no=roll_no
            )
            db.session.add(new_user)
            
            # If Admin, also create Profile (though currently blocked above)
            if role == 'Admin':
                profile = AdminProfile(
                    name=full_name,
                    email=email,
                    phone="", # Default empty
                    school=school_code, # Or a separate school name if available
                    state=""
                )
                db.session.add(profile)
                
            db.session.commit()
            return jsonify({"message": "Account created successfully!"}), 201
            
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Database error: {str(e)}"}), 500

@app.route('/api/check-parent-exists/<school_code>/<roll_no>', methods=['GET'])
def check_parent_exists(school_code, roll_no):
    """
    Check if a parent account already exists for the given student roll number and school code.
    """
    school_code = str(school_code).strip()
    roll_no = str(roll_no).strip()
    
    existing_parent = User.query.filter_by(
        roll_no=roll_no, 
        school_code=school_code, 
        role='Parent'
    ).first()
    
    if existing_parent:
        return jsonify({
            "exists": True, 
            "message": "account is already created"
        }), 200
    
    # Check if student exists at all
    student = Student.query.filter_by(roll_no=roll_no, school_code=school_code).first()
    if not student:
        return jsonify({
            "exists": False, 
            "student_exists": False,
            "message": "Student not found with this roll number."
        }), 200
        
    return jsonify({
        "exists": False, 
        "student_exists": True,
        "message": "Valid student roll number."
    }), 200

@app.route('/add-student', methods=['POST'])
def add_student():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input student data"}), 400
    
    name = data.get('name')
    class_name = data.get('class_name')
    school_code = data.get('school_code')
    
    if not all([name, class_name, school_code]):
        return jsonify({"message": "Name, Class, and School Code are required"}), 400
    
    school_code = str(school_code).strip()

    provided_roll_no = data.get('roll_no')
    
    if provided_roll_no and not Student.query.filter_by(roll_no=provided_roll_no, school_code=school_code).first():
        generated_roll_no = provided_roll_no
    else:
        # Strict Automated Roll Number Generation Logic
        import re
        class_num_match = re.search(r'\d+', str(class_name))
        class_num_int = int(class_num_match.group()) if class_num_match else 0
        
        existing_seq_count = Student.query.filter_by(class_name=class_name, school_code=school_code).count()
        generated_roll_no = str((class_num_int * 100) + existing_seq_count + 1)
    
        if Student.query.filter_by(roll_no=generated_roll_no, school_code=school_code).first():
            existing_val = Student.query.filter_by(class_name=class_name, school_code=school_code) \
                .order_by(Student.id.desc()).first()
            if existing_val and re.search(r'\d+', existing_val.roll_no):
                generated_roll_no = str(int(existing_val.roll_no) + 1)
            else:
                import random
                generated_roll_no = str((class_num_int * 100) + existing_seq_count + random.randint(10,99))

    new_student = Student(
        name=name,
        class_name=class_name,
        roll_no=generated_roll_no,
        school_code=school_code,
        gender=data.get('gender'),
        dob=data.get('dob'),
        family_income=data.get('family_income'),
        parents_occ=data.get('parents_occ'),
        distance=data.get('distance'),
        num_siblings=int(data.get('num_siblings', 0) or 0),
        parent_involv=data.get('parent_involv'),
        parent_name=data.get('parent_name'),
        mobile_number=data.get('mobile_number'),
        address=data.get('address'),
        total_classes=int(data.get('total_classes', 0) or 0),
        present_days=int(data.get('present_days', 0) or 0),
        absent_days=int(data.get('absent_days', 0) or 0),
        base_total_classes=int(data.get('total_classes', 0) or 0),
        base_present_days=int(data.get('present_days', 0) or 0),
        base_absent_days=int(data.get('absent_days', 0) or 0)
    )
    
    try:
        db.session.add(new_student)
        db.session.flush() # Ensure ID is generated for potential alerts
        
        # Calculate Risk AFTER adding to session
        calculate_dropout_risk(new_student)
        
        db.session.commit()
        return jsonify({"message": "Student added successfully and risk evaluated!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Database error: {str(e)}"}), 500

@app.route('/update-student', methods=['POST'])
def update_student():
    data = request.get_json()
    school_code = data.get('school_code')
    roll_no = data.get('roll_no')
    if not roll_no:
        return jsonify({"message": "Roll No is required to update"}), 400
        
    query = Student.query.filter_by(roll_no=roll_no)
    if school_code:
        query = query.filter_by(school_code=school_code)
        
    student = query.first()
    if not student:
        return jsonify({"message": "Student not found in this school"}), 404
        
    # Update fields if provided
    student.name = data.get('name', student.name)
    student.class_name = data.get('class_name', student.class_name)
    student.gender = data.get('gender', student.gender)
    student.dob = data.get('dob', student.dob)
    student.family_income = data.get('family_income', student.family_income)
    student.parents_occ = data.get('parents_occ', student.parents_occ)
    student.distance = data.get('distance', student.distance)
    student.num_siblings = data.get('num_siblings', student.num_siblings)
    student.parent_involv = data.get('parent_involv', student.parent_involv)
    student.parent_name = data.get('parent_name', student.parent_name)
    student.mobile_number = data.get('mobile_number', student.mobile_number)
    student.address = data.get('address', student.address)
    student.total_classes = int(data.get('total_classes', student.total_classes) or 0)
    student.present_days = int(data.get('present_days', student.present_days) or 0)
    student.absent_days = int(data.get('absent_days', student.absent_days) or 0)
    student.base_total_classes = int(data.get('total_classes', student.base_total_classes) or 0)
    student.base_present_days = int(data.get('present_days', student.base_present_days) or 0)
    student.base_absent_days = int(data.get('absent_days', student.base_absent_days) or 0)
    
    # Recalculate risk in case ecosystem factors changed
    calculate_dropout_risk(student)
    
    try:
        db.session.commit()
        return jsonify({"message": "Student updated successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@app.route('/admin/delete-student', methods=['POST'])
def delete_student():
    data = request.get_json()
    admin_email = data.get('admin_email')
    roll_no = data.get('roll_no')
    school_code = data.get('school_code')
    
    # Simple authority check
    admin = User.query.filter(
        User.email == admin_email,
        User.role.in_(['Admin', 'Administrator'])
    ).first()
    if not admin:
        return jsonify({"message": "Only Admins can delete student records"}), 403
        
    query = Student.query.filter_by(roll_no=roll_no)
    if school_code:
        query = query.filter_by(school_code=school_code)
        
    student = query.first()
    if not student:
        return jsonify({"message": "Student not found in this school"}), 404
        
    try:
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": "Student account deleted by Admin"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@app.route('/admin/delete-user', methods=['POST'])
def delete_user():
    data = request.get_json()
    admin_email = data.get('admin_email')
    target_email = data.get('target_email')
    
    # Authority check
    admin = User.query.filter(
        User.email == admin_email,
        User.role.in_(['Admin', 'Administrator'])
    ).first()
    if not admin:
        return jsonify({"message": "Only Admins can delete user accounts"}), 403
        
    user = User.query.filter_by(email=target_email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
        
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"User account {target_email} deleted by Admin"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@app.route('/save-attendance', methods=['GET', 'POST'])
def save_attendance():
    if request.method == 'GET':
        school_code = request.args.get('school_code')
        class_name = request.args.get('class_name')
        date = normalize_date(request.args.get('date'))
        
        # Get all student roll numbers for this class/school
        query = Student.query
        if school_code: query = query.filter_by(school_code=school_code)
        all_students = query.all()
        if class_name:
            norm_target = normalize_class(class_name)
            target_students = [s for s in all_students if normalize_class(s.class_name) == norm_target]
        else:
            target_students = all_students
            
        student_roll_nos = [s.roll_no for s in target_students]
        
        # Fetch logs for these students on this date
        logs = AttendanceLog.query.filter(
            func.trim(AttendanceLog.student_roll_no).in_(student_roll_nos),
            func.trim(AttendanceLog.school_code) == str(school_code).strip(),
            AttendanceLog.entry_date == date
        ).all()
        
        output = []
        for l in logs:
            output.append({
                "roll_no": l.student_roll_no,
                "status": l.status,
                "reason": l.reason or "",
                "session_id": l.session_id,
                "class_name": l.class_name,
                "entry_date": l.entry_date
            })
        return jsonify(output), 200

    """
    Expects bulk attendance for a class.
    Format: {
      "class_name": "10th",
      "date": "2024-03-12",
      "records": [
         {"roll_no": "101", "status": "PRESENT", "reason": ""},
         {"roll_no": "102", "status": "ABSENT", "reason": "Sick"}
      ]
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data"}), 400
        
    class_name = data.get('class_name')
    date = data.get('date')
    school_code = data.get('school_code')
    session_id = data.get('session_id', 'DEFAULT')
    records = data.get('records', [])
    
    if not records:
        return jsonify({"message": "Records are required"}), 400
        
    try:
        updated_count = 0
        log_date = normalize_date(date)
        
        for entry in records:
            roll_no = str(entry.get('roll_no', '')).strip()
            status = normalize_status(entry.get('status', 'PRESENT'))
            reason = entry.get('reason', '')
            student_class = entry.get('class_name') or class_name
            
            # 1. Normalize/Generate session_id
            sid_raw = entry.get('session_id') or session_id
            final_session_id = normalize_session_id(sid_raw)
            
            # 2. Match Student
            query = Student.query.filter_by(roll_no=roll_no)
            if school_code:
                query = query.filter_by(school_code=school_code)
            possible_students = query.all()
            
            student = None
            if student_class:
                norm_target = normalize_class(student_class)
                for s in possible_students:
                    if normalize_class(s.class_name) == norm_target:
                        student = s
                        break
            if not student and possible_students:
                student = possible_students[0]
                
            if student:
                # 3. If no session_id provided, find next available for this specific student
                if final_session_id is None:
                    final_session_id = get_next_session_id(student.roll_no, student.school_code, log_date, student.class_name)
                
                # 4. Check for existing session record
                existing_log = AttendanceLog.query.filter(
                    func.trim(AttendanceLog.student_roll_no) == str(student.roll_no).strip(),
                    func.trim(AttendanceLog.school_code) == str(student.school_code).strip(),
                    AttendanceLog.entry_date == log_date,
                    AttendanceLog.session_id == final_session_id
                ).first()

                if existing_log:
                    existing_log.status = status
                    existing_log.reason = reason
                    existing_log.class_name = student.class_name
                    db.session.flush()
                else:
                    log = AttendanceLog(
                        student_roll_no=student.roll_no, 
                        school_code=student.school_code,
                        class_name=student.class_name,
                        session_id=final_session_id,
                        status=status,
                        reason=reason,
                        entry_date=log_date
                    )
                    db.session.add(log)
                    db.session.flush()
                
                # 5. Recalculate student statistics
                calculate_dropout_risk(student)
                updated_count += 1
        
        db.session.commit()
        print(f"Attendance batch commit successful for {updated_count} records.")
        return jsonify({"message": f"Attendance saved for {updated_count} students.", "status": "Success"}), 200
    except Exception as e:
        import traceback
        with open("attendance_err.log", "a") as f:
            f.write(f"\n[{datetime.utcnow()}] SAVE ATTENDANCE ERROR: {str(e)}\n")
            f.write(traceback.format_exc())
            f.write("\n")
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
@app.route('/mark-attendance', methods=['POST'])
def mark_attendance():
    data = request.get_json()
    roll_no = str(data.get('roll_no') or data.get('roll_number') or "").strip()
    status = normalize_status(data.get('status', 'PRESENT'))
    school_code = data.get('school_code')
    class_name = data.get('class_name')
    
    # 1. Normalize/Auto-generate session_id
    final_session_id = normalize_session_id(data.get('session_id'))
    
    query = Student.query.filter_by(roll_no=roll_no)
    if school_code:
        query = query.filter_by(school_code=school_code)
        
    possible_students = query.all()
    student = None
    if class_name:
        norm_target = normalize_class(class_name)
        for s in possible_students:
            if normalize_class(s.class_name) == norm_target:
                student = s
                break
                
    if not student and possible_students:
        student = possible_students[0]
        
    if not student:
        return jsonify({"message": "Student not found"}), 404
        
    log_date = normalize_date(data.get('date'))
    
    # Auto-generate if not provided/valid
    if final_session_id is None:
        final_session_id = get_next_session_id(student.roll_no, student.school_code, log_date, student.class_name)

    existing_log = AttendanceLog.query.filter(
        func.trim(AttendanceLog.student_roll_no) == str(student.roll_no).strip(),
        func.trim(AttendanceLog.school_code) == str(student.school_code).strip(),
        AttendanceLog.entry_date == log_date,
        AttendanceLog.session_id == final_session_id
    ).first()

    if existing_log:
        existing_log.status = status
        existing_log.reason = data.get('reason', '')
        existing_log.class_name = student.class_name # Ensure synced
        db.session.flush()
    else:
        log = AttendanceLog(
            student_roll_no=student.roll_no, 
            school_code=student.school_code,
            class_name=student.class_name,
            session_id=final_session_id,
            status=status,
            reason=data.get('reason', ''),
            entry_date=log_date
        )
        db.session.add(log)
        db.session.flush()
    
    calculate_dropout_risk(student)
    
    try:
        db.session.commit()
        return jsonify({
            "message": f"Attendance marked as {status} for session {final_session_id}",
            "session_id": final_session_id,
            "attendance_percentage": round(student.attendance_percentage, 2),
            "risk_level": student.risk_level
        }), 200
    except Exception as e:
        import traceback
        with open("attendance_err.log", "a") as f:
            f.write(f"\n[{datetime.utcnow()}] MARK ATTENDANCE ERROR: {str(e)}\n")
            f.write(traceback.format_exc())
            f.write("\n")
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# --- ALERTS SYSTEM APIs ---

@app.route('/api/alerts/send', methods=['POST'])
def send_alert():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data"}), 400
        
    roll_number = data.get('roll_number')
    teacher_name_input = data.get('teacher_name')
    school_code = data.get('school_code')
    
    # Fetch from DB if missing, with strict school isolation if code provided
    if school_code:
        student = Student.query.filter_by(roll_no=roll_number, school_code=school_code).first() if roll_number else None
    else:
        student = Student.query.filter_by(roll_no=roll_number).first() if roll_number else None
        
    teacher = Teacher.query.filter_by(name=teacher_name_input).first() if teacher_name_input else None
    
    student_id_val = student.id if student else None
    class_name_val = student.class_name if student else data.get('class_name', 'Unknown')
    attendance_val = student.attendance if student else None
    
    teacher_id_val = teacher.id if teacher else None
    teacher_name_val = teacher.name if teacher else teacher_name_input

    try:
        new_alert = Alert(
            student_id=student_id_val,
            student_name=data.get('student_name'),
            roll_number=roll_number,
            class_name=class_name_val,
            attendance=attendance_val,
            teacher_id=teacher_id_val,
            teacher_name=teacher_name_val,
            alert_type=data.get('alert_type'),
            alert_message=data.get('alert_message'),
            priority=data.get('priority', 'Low')
        )
        db.session.add(new_alert)
        db.session.commit()
        return jsonify({"message": "Alert sent successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@app.route('/api/alerts/student/<school_code>/<roll_number>', methods=['GET'])
def get_student_alerts(school_code, roll_number):
    student = Student.query.filter_by(roll_no=roll_number, school_code=school_code).first()
    if not student:
        return jsonify([]), 200

    alerts_query = db.session.query(Alert, Teacher).outerjoin(
        Teacher, Alert.teacher_id == Teacher.id
    ).filter(Alert.student_id == student.id).order_by(Alert.date_created.desc()).all()
    
    output = []
    for a, t in alerts_query:
        # User defined logic:
        # Teacher-created alerts MUST show the actual teacher name.
        if t:
            resolved_teacher = t.name
        else:
            resolved_teacher = a.teacher_name or "Unknown Teacher"
        
        output.append({
            "alert_id": a.alert_id,
            "student_name": student.name,
            "roll_number": student.roll_no,
            "attendance": student.attendance,
            "class_name": student.class_name,
            "alert_type": a.alert_type,
            "message": a.alert_message,
            "sent_by": resolved_teacher,
            "priority": a.priority,
            "date": a.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            "status": a.status
        })
    return jsonify(output), 200

@app.route('/api/alerts/student/id/<int:student_id>', methods=['GET'])
def get_alerts_by_id(student_id):
    student = db.session.get(Student, student_id)
    if not student:
        return jsonify([]), 200
        
    alerts_query = db.session.query(Alert, Teacher).outerjoin(
        Teacher, Alert.teacher_id == Teacher.id
    ).filter(Alert.student_id == student.id).order_by(Alert.date_created.desc()).all()
    
    output = []
    for a, t in alerts_query:
        if t:
            resolved_teacher = t.name
        else:
            resolved_teacher = a.teacher_name or "Unknown Teacher"
        
        output.append({
            "alert_id": a.alert_id,
            "student_name": student.name,
            "roll_number": student.roll_no,
            "attendance": student.attendance,
            "class_name": student.class_name,
            "alert_type": a.alert_type,
            "message": a.alert_message,
            "sent_by": resolved_teacher,
            "priority": a.priority,
            "date": a.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            "status": a.status
        })
    return jsonify(output), 200

    return jsonify(output), 200

@app.route('/api/student/<school_code>/<roll_number>', methods=['GET'])
def get_student_by_roll(school_code, roll_number):
    s = Student.query.filter_by(roll_no=roll_number, school_code=school_code).first()
    if not s:
        return jsonify({"message": "Student data not found"}), 404
        
    return jsonify({
        "id": s.id,
        "name": s.name,
        "class_name": s.class_name,
        "roll_no": s.roll_no,
        "school_code": s.school_code,
        "gender": s.gender,
        "dob": s.dob,
        "attendance": s.attendance,
        "attendance_percentage": s.attendance_percentage,
        "risk_level": s.risk_level,
        "mobile_number": s.mobile_number,
        "parent_name": s.parent_name,
        "family_income": s.family_income,
        "parents_occ": s.parents_occ,
        "distance": s.distance,
        "total_classes": int(s.total_classes or 0),
        "present_days": int(s.present_days or 0),
        "absent_days": int(s.absent_days or 0),
        "num_siblings": s.num_siblings,
        "parent_involv": s.parent_involv
    }), 200

@app.route('/api/student/id/<int:student_id>', methods=['GET'])
def get_student_by_id(student_id):
    school_code = request.args.get('school_code')
    s = db.session.get(Student, student_id)
    
    if not s:
        return jsonify({"message": "Student data not found"}), 404
        
    if school_code and str(s.school_code).strip() != str(school_code).strip():
        return jsonify({"message": "Access denied: student belongs to a different school body"}), 403
        
    return jsonify({
        "id": s.id,
        "name": s.name,
        "class_name": s.class_name,
        "roll_no": s.roll_no,
        "school_code": s.school_code,
        "gender": s.gender,
        "dob": s.dob,
        "attendance": s.attendance,
        "attendance_percentage": s.attendance_percentage,
        "risk_level": s.risk_level,
        "mobile_number": s.mobile_number,
        "parent_name": s.parent_name,
        "family_income": s.family_income,
        "parents_occ": s.parents_occ,
        "distance": s.distance,
        "total_classes": int(s.total_classes or 0),
        "present_days": int(s.present_days or 0),
        "absent_days": int(s.absent_days or 0),
        "num_siblings": s.num_siblings,
        "parent_involv": s.parent_involv
    }), 200

@app.route('/api/student/<school_code>/<roll_number>/parent', methods=['POST'])
def update_student_parent(school_code, roll_number):
    s = Student.query.filter_by(roll_no=roll_number, school_code=school_code).first()
    if not s:
        return jsonify({"message": "Student data not found"}), 404
        
    data = request.get_json()
    new_name = data.get('parent_name')
    new_phone = data.get('mobile_number')
    
    if new_name is not None:
        s.parent_name = new_name
    if new_phone is not None:
        s.mobile_number = new_phone
        
    try:
        db.session.commit()
        return jsonify({"message": "Parent profile updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@app.route('/api/alerts/teacher/<teacher_name>', methods=['GET'])
def get_teacher_alerts(teacher_name):
    school_code = request.args.get('school_code')
    class_name = request.args.get('class_name')
    roll_number = request.args.get('roll_no')
    
    query = db.session.query(Alert, Student).outerjoin(
        Student, Alert.student_id == Student.id
    )
    
    query = query.filter(Alert.teacher_name == teacher_name, Alert.date_created <= datetime.utcnow())
    if class_name:
        query = query.filter(db.or_(Alert.class_name == class_name, Student.class_name == class_name))
        
    if school_code:
        query = query.filter(Student.school_code == school_code)
        
    if roll_number:
        query = query.filter(db.or_(Alert.roll_number == roll_number, Student.roll_no == roll_number))
    
    alerts = query.order_by(Alert.date_created.desc()).all()
    
    output = []
    for a, s in alerts:
        resolved_s_name = s.name if s else a.student_name
        resolved_roll = s.roll_no if s else a.roll_number
        resolved_att = s.attendance if s else a.attendance
        resolved_class = s.class_name if s else a.class_name
        
        output.append({
            "alert_id": a.alert_id,
            "student_name": resolved_s_name,
            "roll_number": resolved_roll,
            "attendance": resolved_att,
            "class_name": resolved_class,
            "alert_type": a.alert_type,
            "message": a.alert_message,
            "priority": a.priority,
            "date": a.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            "status": a.status
        })
    return jsonify(output), 200

@app.route('/api/alerts/all', methods=['GET'])
def get_all_alerts():
    school_code = request.args.get('school_code')
    class_name = request.args.get('class_name')

    query = db.session.query(Alert, Student, Teacher).outerjoin(
        Student, Alert.student_id == Student.id
    ).outerjoin(
        Teacher, Alert.teacher_id == Teacher.id
    ).filter(Alert.date_created <= datetime.utcnow())

    if class_name:
        query = query.filter(db.or_(Alert.class_name == class_name, Student.class_name == class_name))
    
    if school_code:
        query = query.filter(Student.school_code == school_code)

    alerts = query.order_by(Alert.date_created.desc()).all()
    
    output = []
    for a, s, t in alerts:
        resolved_s_name = s.name if s else a.student_name
        resolved_roll = s.roll_no if s else a.roll_number
        resolved_att = s.attendance if s else a.attendance
        resolved_class = s.class_name if s else a.class_name
        
        # User defined logic:
        # Teacher-created alerts MUST show the actual teacher name.
        if t:
            resolved_teacher = t.name
        else:
            resolved_teacher = a.teacher_name or "Unknown Teacher"
        
        output.append({
            "alert_id": a.alert_id,
            "teacher_name": resolved_teacher,
            "student_name": resolved_s_name,
            "roll_number": resolved_roll,
            "attendance": resolved_att,
            "class_name": resolved_class,
            "alert_type": a.alert_type,
            "message": a.alert_message,
            "priority": a.priority,
            "date": a.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            "status": a.status
        })
    return jsonify(output), 200

@app.route('/api/alerts/read/<int:alert_id>', methods=['PUT'])
def mark_alert_read(alert_id):
    alert = db.session.get(Alert, alert_id)
    if not alert:
        return jsonify({"message": "Alert not found"}), 404
        
    alert.status = 'Seen'
    try:
        db.session.commit()
        return jsonify({"message": "Alert marked as Seen"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@app.route('/api/alerts/<int:alert_id>', methods=['DELETE'])
def delete_alert(alert_id):
    alert = db.session.get(Alert, alert_id)
    if not alert:
        return jsonify({"message": "Alert not found"}), 404
        
    try:
        db.session.delete(alert)
        db.session.commit()
        return jsonify({"message": "Alert deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@app.route('/add-counseling', methods=['POST'])
def add_counseling():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data"}), 400
        
    new_record = CounselingRecord(
        student_roll_no=data.get('student_roll_no'),
        student_name=data.get('student_name'),
        class_name=data.get('class_name'),
        counselor_name=data.get('counselor_name'),
        session_date=data.get('session_date'),
        counseling_type=data.get('counseling_type'),
        dropout_reason=data.get('dropout_reason'),
        student_mood=data.get('student_mood'),
        progress_status=data.get('progress_status'),
        behavior_observation=data.get('behavior_observation'),
        parent_involvement=data.get('parent_involvement'),
        school_code=str(data.get('school_code', '')).strip(),
        notes=data.get('notes'),
        action_plan=data.get('action_plan'),
        followup_date=data.get('followup_date')
    )
    
    try:
        db.session.add(new_record)
        
        followup_date_str = data.get('followup_date')
        if followup_date_str:
            try:
                parts = followup_date_str.split('-')
                if len(parts) == 3:
                    target_dt = datetime(int(parts[0]), int(parts[1]), int(parts[2]))
                    today = datetime.utcnow()
                    today_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
                    
                    student = Student.query.filter_by(roll_no=data.get('student_roll_no'), school_code=data.get('school_code')).first()
                    teacher = Teacher.query.filter_by(name=data.get('counselor_name')).first()
                    
                    if student and target_dt >= today_date:
                        delta = target_dt - today_date
                        for i in range(delta.days + 1):
                            alert_date = today_date + timedelta(days=i, hours=8)
                            alert = Alert(
                                student_id=student.id,
                                student_name=student.name,
                                roll_number=student.roll_no,
                                class_name=student.class_name,
                                attendance=student.attendance,
                                teacher_id=teacher.id if teacher else None,
                                teacher_name=data.get('counselor_name'),
                                alert_type="Counseling Reminder",
                                alert_message=f"Reminder: Counseling session scheduled on {followup_date_str} for {student.name}.",
                                priority="High",
                                status="Not Seen",
                                date_created=alert_date
                            )
                            db.session.add(alert)
            except Exception as e:
                print(f"Error generating future alerts: {e}")

        db.session.commit()
        return jsonify({"message": "Counseling session recorded successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@app.route('/get-counseling', methods=['GET'])
def get_counseling():
    student_id = request.args.get('student_id')
    roll_no = request.args.get('roll_no')
    counselor_name = request.args.get('counselor_name')
    school_code = request.args.get('school_code')
    class_name = request.args.get('class_name')
    
    query = db.session.query(CounselingRecord, Student).outerjoin(
        Student, 
        db.and_(
            CounselingRecord.student_roll_no == Student.roll_no,
            CounselingRecord.school_code == Student.school_code
        )
    )
    
    if student_id:
        query = query.filter(Student.id == student_id)
    if roll_no:
        query = query.filter(CounselingRecord.student_roll_no == roll_no)
    if school_code:
        query = query.filter(CounselingRecord.school_code == school_code)
    if counselor_name:
        query = query.filter(CounselingRecord.counselor_name == counselor_name)
    if class_name:
        query = query.filter(CounselingRecord.class_name == class_name)
    
    records = query.order_by(CounselingRecord.session_date.desc()).all()
        
    output = []
    for r, s in records:
        resolved_s_name = s.name if s else r.student_name
        resolved_class = s.class_name if s else r.class_name
        
        # Calculate counseling status
        # Logic: If follow_up_date < current date → "Completed", else "Upcoming"
        # If no follow_up_date, default to "Upcoming" or check session_date
        
        status = "Upcoming"
        if r.followup_date:
            try:
                # Expecting yyyy-mm-dd or similar
                # Let's try to parse it
                today = datetime.utcnow().date()
                f_parts = r.followup_date.split('-')
                if len(f_parts) == 3:
                    f_date = datetime(int(f_parts[0]), int(f_parts[1]), int(f_parts[2])).date()
                    if f_date < today:
                        status = "Completed"
                    else:
                        status = "Upcoming"
            except Exception as e:
                print(f"Error parsing followup_date for status: {e}")
        
        output.append({
            "student_roll_no": r.student_roll_no,
            "student_name": resolved_s_name,
            "class_name": resolved_class,
            "counselor_name": r.counselor_name,
            "session_date": r.session_date,
            "counseling_type": r.counseling_type,
            "dropout_reason": r.dropout_reason,
            "student_mood": r.student_mood,
            "progress_status": r.progress_status,
            "behavior_observation": r.behavior_observation,
            "parent_involvement": r.parent_involvement,
            "notes": r.notes,
            "action_plan": r.action_plan,
            "followup_date": r.followup_date,
            "counseling_status": status
        })
    return jsonify(output), 200

@app.route('/get-students', methods=['GET'])
def get_students():
    school_code = request.args.get('school_code')
    class_name = request.args.get('class_name')
    risk_level = request.args.get('risk_level')
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', type=int) # Optional to allow fetching all if none provided
    
    query = Student.query
    if school_code:
        query = query.filter_by(school_code=school_code)
        
    if risk_level and risk_level != "All Risk Levels":
        if "High" in risk_level:
            query = query.filter_by(risk_level="HIGH")
        elif "Medium" in risk_level:
            query = query.filter_by(risk_level="MEDIUM")
        elif "Low" in risk_level:
            query = query.filter_by(risk_level="LOW")
            
    if class_name and str(class_name).strip().lower() != "all classes":
        # Memory filter due to varying class strings
        norm_target = normalize_class(class_name)
        students_all = query.all()
        students = [s for s in students_all if normalize_class(s.class_name) == norm_target]
        print(f"DEBUG: GetStudents - Filtered by Class: {class_name} (norm: {norm_target}), Found: {len(students)}")
        
        if limit is not None:
            start = (page - 1) * limit
            end = start + limit
            students = students[start:end]
    else:
        # Direct DB optimization using lazy queries limit/offset
        if limit is not None:
            query = query.offset((page - 1) * limit).limit(limit)
        students = query.all()
        print(f"DEBUG: GetStudents - Returning All students (No class filter), Total: {len(students)}")
        
    output = []
    for s in students:
        # Fetch latest counseling record for this student
        latest_counseling = CounselingRecord.query.filter_by(
            student_roll_no=s.roll_no, 
            school_code=s.school_code
        ).order_by(CounselingRecord.created_at.desc()).first()
        
        output.append({
            "id": s.id,
            "name": s.name, 
            "class_name": s.class_name, 
            "roll_no": s.roll_no,
            "gender": s.gender, 
            "dob": s.dob, 
            "attendance": s.attendance,
            "attendance_percentage": round(s.attendance_percentage, 2) if s.attendance_percentage is not None else 100.0,
            "risk_level": s.risk_level, 
            "mobile_number": s.mobile_number, 
            "parent_name": s.parent_name,
            "family_income": s.family_income,
            "parents_occ": s.parents_occ,
            "distance": s.distance,
            "address": s.address,
            "total_classes": s.total_classes or 0,
            "present_days": s.present_days or 0,
            "absent_days": s.absent_days or 0,
            "num_siblings": s.num_siblings,
            "parent_involv": s.parent_involv,
            "address": s.address,
            "school_code": s.school_code,
            "last_counseling_date": latest_counseling.session_date if latest_counseling else "None",
            "follow_up_status": latest_counseling.followup_date if (latest_counseling and latest_counseling.followup_date) else "Pending"
        })
    return jsonify(output), 200

@app.route('/get-student/<student_id>', methods=['GET'])
def get_student(student_id):
    # Handle composite IDs like "db_101" from some frontend mocks
    real_id = student_id
    if "_" in str(student_id):
        real_id = str(student_id).split("_")[-1]
    
    school_code = request.args.get('school_code')
    try:
        student = db.session.get(Student, int(real_id))
    except:
        # If it was a roll_no instead
        query = Student.query.filter_by(roll_no=student_id)
        if school_code:
            query = query.filter_by(school_code=school_code)
        student = query.first()
        
    if student and school_code and str(student.school_code).strip() != str(school_code).strip():
        return jsonify({"message": "Access denied: student belongs to a different school body"}), 403

    if not student:
        return jsonify({"message": "Student not found"}), 404
    
    # Fetch latest counseling record for this student
    latest_counseling = CounselingRecord.query.filter_by(
        student_roll_no=student.roll_no, 
        school_code=student.school_code
    ).order_by(CounselingRecord.created_at.desc()).first()
    
    return jsonify({
        "id": student.id,
        "name": student.name, 
        "class_name": student.class_name, 
        "roll_no": student.roll_no,
        "gender": student.gender, 
        "dob": student.dob, 
        "attendance": student.attendance,
        "attendance_percentage": round(student.attendance_percentage, 2) if student.attendance_percentage is not None else 100.0,
        "risk_level": student.risk_level, 
        "mobile_number": student.mobile_number, 
        "parent_name": student.parent_name,
        "family_income": student.family_income,
        "parents_occ": student.parents_occ,
        "distance": student.distance,
        "address": student.address,
        "total_classes": student.total_classes or 0,
        "present_days": student.present_days or 0,
        "absent_days": student.absent_days or 0,
        "num_siblings": student.num_siblings,
        "num_siblings": student.num_siblings,
        "parent_involv": student.parent_involv,
        "school_code": student.school_code,
        "last_counseling_date": latest_counseling.session_date if latest_counseling else "None",
        "follow_up_status": latest_counseling.followup_date if (latest_counseling and latest_counseling.followup_date) else "Pending"
    }), 200

@app.route('/student-stats', methods=['GET'])
def student_stats():
    school_code = request.args.get('school_code')
    class_name = request.args.get('class_name')
    
    query = Student.query
    if school_code:
        query = query.filter(Student.school_code == school_code)
        
    students = query.all()
    if class_name:
        norm_target = normalize_class(class_name)
        students = [s for s in students if normalize_class(s.class_name) == norm_target]
    
    stats = {
        "total_students": len(students),
        "high_risk_count": 0,
        "low_risk_count": 0,
        "medium_risk_count": 0
    }
    
    for s in students:
        if s.risk_level == 'HIGH': stats["high_risk_count"] += 1
        elif s.risk_level == 'LOW': stats["low_risk_count"] += 1
        elif s.risk_level == 'MEDIUM': stats["medium_risk_count"] += 1
        
    return jsonify(stats), 200

@app.route('/api/teacher/login', methods=['POST'])
@app.route('/api/admin/login', methods=['POST'])
@app.route('/api/parent/login', methods=['POST'])
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    # Auto-detect role if missing based on URL
    path_norm = request.path.lower()
    if 'teacher' in path_norm:
        role_default = 'Teacher'
    elif 'admin' in path_norm:
        role_default = 'Admin'
    elif 'parent' in path_norm:
        role_default = 'Parent'
    else:
        role_default = 'Admin'
        
    role = str(data.get('role') or role_default).strip().title()
    if role == 'Administrator':
        role = 'Admin'
    school_code = str(data.get('school_code', '')).strip()
    password = str(data.get('password', '')).strip()
    
    if not school_code:
        return jsonify({"message": "Please enter school code"}), 400

    print(f"DEBUG: Login Attempt - Role: {role}, School: {school_code}")

    # 1. First validate if the school code exists in the database across relevant tables
    user_exists = User.query.filter_by(school_code=school_code).first() is not None
    teacher_exists = Teacher.query.filter_by(school_code=school_code).first() is not None
    student_exists = Student.query.filter_by(school_code=school_code).first() is not None
    
    if not any([user_exists, teacher_exists, student_exists]):
        return jsonify({"message": "Invalid school code"}), 404

    user = None
    # Selection based on role
    if role == 'Admin':
        email = data.get('email', '').strip()
        print(f"DEBUG: Admin Log - Email: {email}")
        if not all([email, password]):
            return jsonify({"message": "Please enter email and password"}), 400
        
        user = User.query.filter(
            func.lower(func.trim(User.email)) == email.lower(),
            func.trim(User.school_code) == school_code.strip(),
            db.or_(User.role == 'Admin', User.role == 'Administrator')
        ).first()
        
        if not user:
            # Check if user exists but at a different school for better messaging
            other_school = User.query.filter(
                func.lower(func.trim(User.email)) == email.lower(),
                db.or_(User.role == 'Admin', User.role == 'Administrator')
            ).first()
            
            if other_school:
                print(f"DEBUG: Admin Log - User found at different school: {other_school.school_code}")
                return jsonify({"message": f"This account is registered for school code {other_school.school_code}"}), 401
            else:
                print(f"DEBUG: Admin Log - No admin user found for email '{email}'")
                return jsonify({"message": "Invalid email or role"}), 401
        
        if user.password.strip() != password.strip():
            print(f"DEBUG: Admin Log - Password mismatch for {email}. DB: '{user.password.strip()}', Input: '{password.strip()}'")
            return jsonify({"message": "Invalid password"}), 401

    elif role == 'Teacher':
        identity = str(data.get('email') or data.get('username') or '').strip()
        class_entered = str(data.get('class_assigned') or data.get('class_name') or '').strip()
        
        if not all([identity, password, class_entered]):
            return jsonify({"message": "Please fill all required fields."}), 400
            
        print(f"DEBUG: Teacher Login Attempt - Identity: '{identity}', Class: '{class_entered}'")

        teacher_record = Teacher.query.filter(
            db.and_(
                db.or_(
                    func.lower(Teacher.email) == identity.lower(),
                    Teacher.teacher_id == identity
                ),
                Teacher.school_code == school_code
            )
        ).first()
        
        if not teacher_record:
            return jsonify({"message": "Invalid credentials for this school code"}), 401
            
        if teacher_record.password != password:
            return jsonify({"message": "Invalid credentials for this school code"}), 401
            
        if normalize_class(teacher_record.class_assigned) != normalize_class(class_entered):
             return jsonify({"message": "This class is not assigned to you."}), 401
             
        user = teacher_record

    elif role == 'Parent':
        roll_no = str(data.get('roll_no', '')).strip()
        print(f"DEBUG: Parent RollNo: '{roll_no}', SchoolCode: '{school_code}'")
        
        if not all([roll_no, password]):
            return jsonify({"message": "Please enter Roll No and password"}), 400
            
        user = User.query.filter_by(roll_no=roll_no, school_code=school_code, role='Parent').first()
        
        if not user or user.password != password:
            return jsonify({"message": "Invalid credentials for this school code"}), 401
            
        student_record = Student.query.filter_by(roll_no=roll_no, school_code=school_code).first()
        
        if not student_record:
            return jsonify({"message": "Student data not found"}), 404
            
        current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        user.login_time = current_time
        user.status = 'Active'
        db.session.commit()
        
        return jsonify({
            "message": "Login successful",
            "user": {
                "full_name": student_record.name,
                "role": role,
                "class_assigned": student_record.class_name
            },
            "student_data": {
                "id": student_record.id,
                "name": student_record.name,
                "class_name": student_record.class_name,
                "roll_no": student_record.roll_no,
                "school_code": student_record.school_code,
                "gender": student_record.gender,
                "dob": student_record.dob,
                "attendance": student_record.attendance,
                "attendance_percentage": student_record.attendance_percentage,
                "risk_level": student_record.risk_level,
                "mobile_number": student_record.mobile_number,
                "parent_name": student_record.parent_name,
                "family_income": student_record.family_income,
                "parents_occ": student_record.parents_occ,
                "distance": student_record.distance,
                "total_classes": student_record.total_classes,
                "present_days": student_record.present_days,
                "absent_days": student_record.absent_days,
                "num_siblings": student_record.num_siblings,
                "parent_involv": student_record.parent_involv
            }
        }), 200
    
    else:
        return jsonify({"message": "Invalid role specified"}), 400

    if user and user.password == password:
        current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        if role == 'Teacher':
            tracked_teacher = User.query.filter_by(email=user.email, role='Teacher').first()
            if not tracked_teacher:
                tracked_teacher = User(
                    full_name=user.name,
                    email=user.email,
                    password=user.password,
                    role='Teacher',
                    school_code=user.school_code,
                    class_assigned=user.class_assigned
                )
                db.session.add(tracked_teacher)
            tracked_teacher.login_time = current_time
            tracked_teacher.status = 'Active'
            tracked_teacher.password = user.password # Sync password from teachers table
        else:
            user.login_time = current_time
            user.status = 'Active'
            
        db.session.commit()

        user_response = {
            "full_name": user.full_name if hasattr(user, 'full_name') else user.name,
            "role": role
        }
        
        # Only include class_assigned for Teachers, not for Admins
        if role == 'Teacher':
            user_response["class_assigned"] = user.class_assigned if hasattr(user, 'class_assigned') else None
            
        return jsonify({
            "message": "Login successful",
            "user": user_response
        }), 200
    else:
        return jsonify({"message": "Invalid credentials for this school code"}), 401

# ── Teacher Management ──────────────────────────────────────────────────────

@app.route('/api/admin/add-teacher', methods=['POST'])
@app.route('/add-teacher', methods=['POST'])
def add_teacher():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400
    
    email = data.get('email')
    existing_teacher = Teacher.query.filter_by(email=email).first()
    if existing_teacher:
        return jsonify({"message": "Email already exists"}), 400

    new_teacher = Teacher(
        teacher_id=data.get('teacher_id'),
        name=data.get('name'),
        email=email,
        password=data.get('password'),
        subject=data.get('subject'),
        phone=data.get('phone'),
        class_assigned=data.get('class_assigned'),
        school_code=data.get('school_code'),
        status='APPROVED'
    )
    
    try:
        db.session.add(new_teacher)
        db.session.commit()
        return jsonify({"message": "Teacher registered for approval!"}), 201
    except Exception as e:
        import traceback
        with open("debug_teacher.log", "a") as f:
            f.write("\\n--- ADD TEACHER ERROR ---\\n")
            f.write(traceback.format_exc())
            f.write("\\n")
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@app.route('/api/admin/get-teachers', methods=['GET'])
@app.route('/get-teachers', methods=['GET'])
def get_teachers():
    school_code = request.args.get('school_code')
    query = Teacher.query
    if school_code:
        query = query.filter_by(school_code=school_code)
        
    teachers = query.all()
    output = []
    for t in teachers:
        output.append({
            "id": t.id,
            "teacher_id": t.teacher_id,
            "name": t.name,
            "email": t.email,
            "subject": t.subject,
            "phone": t.phone,
            "class_assigned": t.class_assigned,
            "school_code": t.school_code,
            "status": t.status
        })
    return jsonify(output), 200

@app.route('/update-teacher-status', methods=['POST'])
def update_teacher_status():
    data = request.get_json()
    teacher_id = data.get('id')
    new_status = data.get('status')
    
    teacher = db.session.get(Teacher, teacher_id)
    if not teacher:
        return jsonify({"message": "Teacher not found"}), 404
    
    teacher.status = new_status

    
    try:
        db.session.commit()
        return jsonify({"message": f"Teacher {new_status.lower()} successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@app.route('/create-teacher-account', methods=['POST'])
def create_teacher_account():
    data = request.get_json()
    teacher_id = data.get('id')
    email = data.get('email')
    password = data.get('password')
    
    teacher = db.session.get(Teacher, teacher_id)
    if not teacher:
        return jsonify({"message": "Teacher not found"}), 404
        
    if teacher.status != 'APPROVED':
        return jsonify({"message": "Teacher must be officially Approved before an account can be created."}), 400
        
    if not password or not email:
        return jsonify({"message": "Email and password must be provided."}), 400
        
    teacher.email = email
    teacher.password = password
    
    try:
        db.session.commit()
        return jsonify({"message": "Account successfully created!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# ── Dashboard Insights ──────────────────────────────────────────────────────

@app.route('/recent-high-risk', methods=['GET'])
def recent_high_risk():
    school_code = request.args.get('school_code')
    class_name = request.args.get('class_name')
    
    query = Student.query.filter_by(risk_level='HIGH')
    if school_code:
        query = query.filter_by(school_code=school_code)
        
    students = query.order_by(Student.created_at.desc()).all()
    if class_name:
        norm_target = normalize_class(class_name)
        students = [s for s in students if normalize_class(s.class_name) == norm_target]
        
    high_risk_students = students[:3]
    output = []
    for s in high_risk_students:
        output.append({
            "name": s.name,
            "class_name": s.class_name,
            "attendance": f"{s.attendance_percentage}%"
        })
    return jsonify(output), 200

# ── Teacher Profile Endpoints ────────────────────────────────────────────────

@app.route('/api/teacher/profile', methods=['GET'])
@app.route('/get-teacher-profile', methods=['GET'])
def get_teacher_profile():
    email = request.args.get('email', '').strip().lower()
    if not email:
        return jsonify({"message": "Email is required"}), 400
    
    print(f"DEBUG: Fetching Teacher Profile for: {email}")
    teacher = Teacher.query.filter(func.lower(Teacher.email) == email).first()
    if not teacher:
        return jsonify({"message": "Teacher not found"}), 404
    
    return jsonify({
        "name": teacher.name,
        "teacher_id": teacher.teacher_id,
        "email": teacher.email,
        "phone": teacher.phone,
        "gender": teacher.gender,
        "school": teacher.school_code,
        "school_code": teacher.school_code,
        "class_assigned": teacher.class_assigned
    }), 200

@app.route('/api/teacher/profile/update', methods=['POST'])
@app.route('/update-teacher-profile', methods=['POST'])
def update_teacher_profile():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400
        
    # Identify target via email (which is locked in UI) or teacher_id
    target_email = data.get('old_email') or data.get('email')
    teacher_id = data.get('teacher_id')
    
    teacher = None
    if target_email:
        teacher = Teacher.query.filter_by(email=target_email).first()
    if not teacher and teacher_id:
        teacher = Teacher.query.filter_by(teacher_id=teacher_id).first()

    if not teacher:
        return jsonify({"message": f"Teacher profile not found for identifier: {target_email or teacher_id}"}), 404
        
    # Update Teacher table directly
    new_email = data.get('email', teacher.email)
    teacher.email = new_email
    teacher.name = data.get('name', teacher.name)
    teacher.phone = data.get('phone', teacher.phone)
    teacher.gender = data.get('gender', teacher.gender)
    teacher.subject = data.get('subject', teacher.subject)
    teacher.class_assigned = data.get('class_assigned', teacher.class_assigned)

    try:
        db.session.commit()
        return jsonify({"message": "Teacher profile updated successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@app.route('/change-password', methods=['POST'])
def change_password():
    data = request.get_json()
    email = data.get('email')
    role = str(data.get('role') or 'Admin').strip().title()
    if role == 'Administrator':
        role = 'Admin'
    current_password = data.get('old_password') or data.get('current_password')
    new_password = data.get('new_password')
    school_code = data.get('school_code')
    
    if not all([email, current_password, new_password]):
        return jsonify({"success": False, "message": "Missing required fields"}), 400
        
    user = None
    if role == 'Teacher':
        user = Teacher.query.filter_by(email=email).first()
    elif role == 'Parent':
        if school_code:
            user = User.query.filter_by(roll_no=email, school_code=school_code, role='Parent').first()
        else:
            user = User.query.filter_by(roll_no=email, role='Parent').first()
    else:
        user = User.query.filter_by(email=email, role=role).first()
        
    if not user:
        return jsonify({"success": False, "message": f"{role} user not found"}), 404
        
    if user.password != current_password:
        return jsonify({"success": False, "message": "Incorrect current password"}), 401
        
    user.password = new_password
    
    # Keep the unified tracking table (User) in sync with the Teacher/Parent specific tables if needed
    if role == 'Teacher':
        track_user = User.query.filter_by(email=email, role='Teacher').first()
        if track_user:
            track_user.password = new_password

    try:
        db.session.commit()
        return jsonify({"success": True, "message": "Password updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

# ── Forgot Password Flow ───────────────────────────────────────────────────

@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    role = str(data.get('role') or '').strip().title()
    if role == 'Administrator':
        role = 'Admin'

    if not email or not role:
        return jsonify({"message": "Email and role are required"}), 400

    user = None
    if role == 'Admin':
        user = User.query.filter(
            User.email == email,
            User.role.in_(['Admin', 'Administrator'])
        ).first()
    elif role == 'Teacher':
        user = Teacher.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": f"No account found with this email for role {role}"}), 404

    # Generate OTP
    otp_code = f"{random.randint(100000, 999999)}"
    expires_at = datetime.utcnow() + timedelta(minutes=10)

    # Invalidate previous OTPs for this email and role
    OTP.query.filter_by(email=email, role=role).delete()

    new_otp = OTP(email=email, role=role, otp_code=otp_code, expires_at=expires_at)
    db.session.add(new_otp)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Exception creating OTP: {e}")
        return jsonify({"message": f"Error generating OTP: {str(e)}"}), 500

    # Send OTP
    if send_otp_email(email, otp_code):
        return jsonify({"message": "OTP sent successfully to your email"}), 200
    else:
        # Delete OTP from DB if email sending failed
        OTP.query.filter_by(id=new_otp.id).delete()
        db.session.commit()
        return jsonify({"message": "Failed to send OTP email"}), 500

@app.route('/api/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email')
    role = str(data.get('role') or '').strip().title()
    if role == 'Administrator':
        role = 'Admin'
    otp_code = data.get('otp_code')

    if not all([email, role, otp_code]):
        return jsonify({"message": "Email, role, and OTP code are required"}), 400

    otp_record = OTP.query.filter_by(email=email, role=role, otp_code=otp_code).first()

    if not otp_record:
        return jsonify({"message": "Invalid OTP"}), 400

    if not otp_record.is_valid():
        db.session.delete(otp_record)
        db.session.commit()
        return jsonify({"message": "OTP has expired"}), 400

    return jsonify({"message": "OTP verified successfully"}), 200

@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    role = str(data.get('role') or '').strip().title()
    if role == 'Administrator':
        role = 'Admin'
    otp_code = data.get('otp_code')
    new_password = data.get('new_password')

    if not all([email, role, otp_code, new_password]):
        return jsonify({"message": "Missing required fields"}), 400

    # Verify OTP again to be secure
    otp_record = OTP.query.filter_by(email=email, role=role, otp_code=otp_code).first()

    if not otp_record or not otp_record.is_valid():
        return jsonify({"message": "Invalid or expired OTP"}), 400

    if role == 'Admin':
        user = User.query.filter(
            User.email == email,
            User.role.in_(['Admin', 'Administrator'])
        ).first()
    elif role == 'Teacher':
        user = Teacher.query.filter_by(email=email).first()
    else:
        return jsonify({"message": "Invalid role"}), 400

    if not user:
        return jsonify({"message": "User not found"}), 404

    user.password = new_password
    
    # Stay synced
    if role == 'Teacher':
        track_user = User.query.filter_by(email=email, role='Teacher').first()
        if track_user:
            track_user.password = new_password

    db.session.delete(otp_record) # Remove used OTP

    try:
        db.session.commit()
        return jsonify({"message": "Password reset successfully. You can now login with your new password."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


@app.route('/api/student/<student_id>/risk-history', methods=['GET'])
def get_student_risk_history(student_id):
    school_code = request.args.get('school_code')
    # Handle composite IDs like "db_101"
    real_id = student_id
    if "_" in str(student_id):
        real_id = str(student_id).split("_")[-1]
        
    try:
        query = RiskHistory.query.filter_by(student_id=int(real_id))
        
        # Verify student exists in this school if code provided
        student = db.session.get(Student, int(real_id))
        if student and school_code and str(student.school_code).strip() != str(school_code).strip():
            return jsonify({"message": "Access denied"}), 403
            
        history = query.order_by(RiskHistory.date_recorded.desc()).all()
    except:
        # Fallback to current database behavior if id not numeric
        student = Student.query.filter_by(roll_no=student_id).first()
        if student:
            history = RiskHistory.query.filter_by(student_id=student.id).order_by(RiskHistory.date_recorded.desc()).all()
        else:
            history = []
            
    output = []
    
    # If no history exists, generate an initial history point from the current student record
    if not history:
        student = db.session.get(Student, student_id)
        if student:
            output.append({
                "risk_level": student.risk_level,
                "date": student.created_at.strftime('%d %b %Y') if student.created_at else datetime.utcnow().strftime('%d %b %Y')
            })
    else:
        for h in history:
            output.append({
                "risk_level": h.risk_level,
                "date": h.date_recorded.strftime('%d %b %Y')
            })
            
    return jsonify(output), 200

@app.route('/api/student/<school_code>/<roll_no>/risk-history', methods=['GET'])
def get_student_risk_history_v2(school_code, roll_no):
    student = Student.query.filter_by(roll_no=roll_no, school_code=school_code).first()
    if not student:
        return jsonify([]), 200
    return get_student_risk_history(student.id)

# --- UNIFIED ADMIN PROFILE MANAGEMENT ---
@app.route('/api/admin/profile/<id_or_email>', methods=['GET', 'POST', 'PUT'])
@app.route('/api/admin/profile/update', methods=['POST', 'PUT'])
@app.route('/update-admin-profile', methods=['POST', 'PUT'])
@app.route('/get-admin-profile', methods=['GET'])
def handle_admin_profile(id_or_email=None):
    data = request.get_json() if request.method in ['POST', 'PUT'] else {}
    
    # Identify target via URL param, query param, or body
    target = id_or_email or request.args.get('email') or data.get('email')
    
    if not target:
        return jsonify({"success": False, "message": "Email or ID is required"}), 400
        
    # Lookup by ID (if numeric) or Email
    admin = None
    if str(target).isdigit():
        admin = db.session.get(AdminProfile, int(target))
    
    if not admin:
        admin = AdminProfile.query.filter_by(email=target).first()
        
    if request.method == 'GET':
        if not admin:
             # Check if user exists as admin and auto-create profile
             user = User.query.filter(User.email == target, User.role.in_(['Admin', 'Administrator'])).first()
             if user:
                 admin = AdminProfile(email=target, name=user.full_name, role='Administrator')
                 db.session.add(admin)
                 db.session.commit()
             else:
                 return jsonify({"success": False, "message": "Admin profile not found"}), 404
        
        return jsonify({
            "success": True,
            "name": admin.name,
            "email": admin.email,
            "phone": admin.phone,
            "gender": admin.gender,
            "role": admin.role,
            "school": admin.school,
            "state": admin.state
        }), 200

    elif request.method in ['POST', 'PUT']:
        if not admin:
            # Check if user existed to allow profile creation
            req_email = data.get('email') or (target if "@" in str(target) else None)
            if not req_email:
                return jsonify({"success": False, "message": "Admin profile not found and no email provided to create one"}), 404
                
            user = User.query.filter(User.email == req_email, User.role.in_(['Admin', 'Administrator'])).first()
            if user:
                admin = AdminProfile(email=req_email, name=data.get('name', user.full_name))
                db.session.add(admin)
            else:
                return jsonify({"success": False, "message": "Admin user account not found"}), 404
        
        # Update fields
        admin.name = data.get('name', admin.name)
        admin.phone = data.get('phone', admin.phone)
        admin.gender = data.get('gender', admin.gender)
        admin.school = data.get('school', admin.school)
        admin.state = data.get('state', admin.state)
        
        # Sync name with User table if it exists
        user = User.query.filter_by(email=admin.email).first()
        if user:
            user.full_name = admin.name
            
        try:
            db.session.commit()
            return jsonify({"success": True, "message": "Profile updated successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host=app.config['FLASK_HOST'], port=app.config['FLASK_PORT'])

