import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database Configuration (MySQL)
    DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    DB_NAME = os.environ.get("DB_NAME", "vidhyarakshak")

    # SQLAlchemy Configuration
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 280,
        "pool_pre_ping": True,
    }

    # Flask Configuration
    SECRET_KEY = os.environ.get("SECRET_KEY", "vidhyarakshak_secret")
    FLASK_HOST = "0.0.0.0"
    FLASK_PORT = 5000
    DEBUG = True

    # SMTP Configuration (Optional)
    SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
    SMTP_USER = os.environ.get("SMTP_USER", "vidhyarakshaka@gmail.com")
    SMTP_APP_PASSWORD = os.environ.get("SMTP_APP_PASSWORD", "fscieejwvzkplagn")
