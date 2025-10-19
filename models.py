"""
Database models for Grievance Filing Service
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User account model"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    user_type = db.Column(db.String(20), nullable=False)  # 'consumer' or 'realtor'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    complaints = db.relationship('Complaint', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


class Complaint(db.Model):
    """Complaint/grievance model"""
    __tablename__ = 'complaints'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Complaint details
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default='draft')  # draft, submitted, under_review, closed
    jurisdiction_type = db.Column(db.String(50))  # state_board, nar_association, civil_court
    state = db.Column(db.String(50))

    # Respondent information
    respondent_name = db.Column(db.String(200))
    respondent_license_number = db.Column(db.String(100))
    respondent_brokerage = db.Column(db.String(200))
    respondent_is_realtor = db.Column(db.Boolean, default=False)

    # Incident details
    incident_date = db.Column(db.Date)
    incident_location = db.Column(db.String(200))
    transaction_type = db.Column(db.String(100))  # buyer, seller, lease, etc.

    # Complaint narrative
    complaint_narrative = db.Column(db.Text)
    alleged_violations = db.Column(db.Text)  # JSON string of Article numbers and descriptions

    # Timeline tracking
    filing_deadline = db.Column(db.Date)
    submitted_date = db.Column(db.Date)
    investigation_expected_completion = db.Column(db.Date)

    # Administrative
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    documents = db.relationship('Document', backref='complaint', lazy=True, cascade='all, delete-orphan')
    notes = db.relationship('Note', backref='complaint', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Complaint {self.id}: {self.title}>'


class Document(db.Model):
    """Document upload model"""
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.id'), nullable=False)

    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(50))  # contract, correspondence, check, listing_agreement, etc.
    file_size = db.Column(db.Integer)  # in bytes

    description = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Document {self.original_filename}>'


class Note(db.Model):
    """Notes/updates on complaint progress"""
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.id'), nullable=False)

    content = db.Column(db.Text, nullable=False)
    note_type = db.Column(db.String(50), default='user')  # user, system, status_update
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Note {self.id} for Complaint {self.complaint_id}>'


class Reminder(db.Model):
    """Deadline reminders"""
    __tablename__ = 'reminders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.id'))

    reminder_date = db.Column(db.DateTime, nullable=False)
    reminder_type = db.Column(db.String(50))  # filing_deadline, document_request, follow_up
    message = db.Column(db.Text)
    is_sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Reminder {self.id} for User {self.user_id}>'
