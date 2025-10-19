"""
Configuration settings for Grievance Filing Service
"""
import os
from datetime import timedelta

class Config:
    """Base configuration"""

    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Database settings
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{os.path.join(BASE_DIR, "database.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx', 'txt'}

    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

    # Email settings (for future notification system)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # Jurisdiction-specific deadline settings (in days)
    DEADLINE_SETTINGS = {
        'NAR_ETHICS': 180,  # 180 days after offense for NAR ethics complaints
        'KENTUCKY': 365,    # 1 year for Kentucky complaints
        'FLORIDA': 730,     # 2 years for Florida (example)
        'COLORADO': 365,    # 1 year for Colorado (example)
        'DEFAULT': 180      # Default fallback
    }

    # Investigation timeline estimates (in days)
    INVESTIGATION_TIMELINES = {
        'COLORADO': 240,
        'DEFAULT': 180
    }
