from app import app, db, AttendanceLog
from datetime import datetime

def normalize_all_dates():
    with app.app_context():
        print("Normalizing all existing logs' dates...")
        logs = AttendanceLog.query.all()
        for l in logs:
            raw = l.entry_date
            if not raw: continue
            
            try:
                # Try various formats
                normalized = None
                if '/' in raw:
                    parts = raw.split('/')
                    if len(parts) == 3:
                        d, m, y = int(parts[0]), int(parts[1]), int(parts[2])
                        normalized = f"{d:02d}/{m:02d}/{y}"
                elif '-' in raw:
                    parts = raw.split('-')
                    if len(parts) == 3:
                        # yyyy-mm-dd assumed
                        if len(parts[0]) == 4:
                            y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
                            normalized = f"{d:02d}/{m:02d}/{y}"
                        else:
                            d, m, y = int(parts[0]), int(parts[1]), int(parts[2])
                            normalized = f"{d:02d}/{m:02d}/{y}"
                
                if normalized and l.entry_date != normalized:
                    print(f"Normalizing {l.entry_date} -> {normalized}")
                    l.entry_date = normalized
            except Exception as e:
                print(f"Error on {raw}: {e}")

        db.session.commit()
        print("Date normalization complete!")

if __name__ == "__main__":
    normalize_all_dates()
