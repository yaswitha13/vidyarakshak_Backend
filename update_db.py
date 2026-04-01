from app import app, db, Alert

with app.app_context():
    # Only drop and recreate the alerts table
    Alert.__table__.drop(db.engine)
    db.create_all()
    print("Alerts table dropped and recreated with new schema!")
