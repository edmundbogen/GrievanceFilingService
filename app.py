"""
Grievance Filing Service - Main Flask Application
Assists consumers and REALTORS® in filing complaints against real estate professionals
"""
import os
import json
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from config import Config
from models import db, User, Complaint, Document, Note, Reminder
from utils.nar_code_articles import get_all_articles, get_article, search_articles, get_articles_list
from utils.deadline_calculator import (
    calculate_filing_deadline,
    calculate_reminder_dates,
    days_until_deadline,
    get_deadline_status,
    estimate_investigation_completion
)
from utils.state_forms import (
    get_state_requirements,
    get_nar_requirements,
    get_all_states,
    get_required_documents,
    get_filing_checklist
)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# ==================== ROUTES ====================

@app.route('/')
def index():
    """Homepage"""
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        user_type = request.form.get('user_type')

        # Check if user exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please login.', 'warning')
            return redirect(url_for('login'))

        # Create new user
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            user_type=user_type
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.first_name}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard showing all complaints"""
    complaints = Complaint.query.filter_by(user_id=current_user.id).order_by(Complaint.updated_at.desc()).all()

    # Add deadline status to each complaint
    for complaint in complaints:
        if complaint.filing_deadline:
            complaint.deadline_info = get_deadline_status(complaint.filing_deadline)
        else:
            complaint.deadline_info = None

    return render_template('dashboard.html', complaints=complaints)


@app.route('/jurisdiction-screening', methods=['GET', 'POST'])
@login_required
def jurisdiction_screening():
    """Questionnaire to determine proper jurisdiction"""
    if request.method == 'POST':
        # Store screening results in session
        session['screening'] = {
            'is_realtor': request.form.get('is_realtor') == 'yes',
            'violation_type': request.form.get('violation_type'),
            'state': request.form.get('state'),
            'has_contract': request.form.get('has_contract') == 'yes',
            'seeks_damages': request.form.get('seeks_damages') == 'yes'
        }

        # Determine jurisdiction
        screening = session['screening']
        jurisdiction = determine_jurisdiction(screening)
        session['jurisdiction'] = jurisdiction

        flash(f'Based on your answers, your complaint should be filed with: {jurisdiction["agency"]}', 'info')
        return redirect(url_for('new_complaint'))

    states = get_all_states()
    return render_template('jurisdiction_screening.html', states=states)


def determine_jurisdiction(screening):
    """Determine appropriate jurisdiction based on screening"""
    if screening['seeks_damages'] or screening['violation_type'] == 'contract_dispute':
        return {
            'type': 'civil_court',
            'agency': 'Civil Court / Attorney',
            'message': 'This appears to be a contract dispute. You may need to consult an attorney or file in civil court.'
        }

    if screening['is_realtor'] and screening['violation_type'] == 'ethics_violation':
        return {
            'type': 'nar_association',
            'agency': 'Local REALTOR® Association',
            'message': 'This is an ethics complaint against a NAR member. File with your local REALTOR® association.'
        }

    return {
        'type': 'state_board',
        'agency': f'{screening["state"]} Real Estate Commission',
        'message': 'This is a license law complaint. File with your state licensing board.'
    }


@app.route('/complaint/new', methods=['GET', 'POST'])
@login_required
def new_complaint():
    """Create new complaint"""
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        jurisdiction_type = request.form.get('jurisdiction_type')
        state = request.form.get('state')

        # Respondent info
        respondent_name = request.form.get('respondent_name')
        respondent_license_number = request.form.get('respondent_license_number')
        respondent_brokerage = request.form.get('respondent_brokerage')
        respondent_is_realtor = request.form.get('respondent_is_realtor') == 'yes'

        # Incident details
        incident_date_str = request.form.get('incident_date')
        incident_date = datetime.strptime(incident_date_str, '%Y-%m-%d').date() if incident_date_str else None
        incident_location = request.form.get('incident_location')
        transaction_type = request.form.get('transaction_type')

        # Narrative
        complaint_narrative = request.form.get('complaint_narrative')

        # Selected NAR articles (if applicable)
        selected_articles = request.form.getlist('nar_articles')
        alleged_violations = json.dumps(selected_articles) if selected_articles else None

        # Calculate deadline
        filing_deadline = calculate_filing_deadline(incident_date, jurisdiction_type, state)

        # Create complaint
        complaint = Complaint(
            user_id=current_user.id,
            title=title,
            jurisdiction_type=jurisdiction_type,
            state=state,
            respondent_name=respondent_name,
            respondent_license_number=respondent_license_number,
            respondent_brokerage=respondent_brokerage,
            respondent_is_realtor=respondent_is_realtor,
            incident_date=incident_date,
            incident_location=incident_location,
            transaction_type=transaction_type,
            complaint_narrative=complaint_narrative,
            alleged_violations=alleged_violations,
            filing_deadline=filing_deadline
        )

        db.session.add(complaint)
        db.session.commit()

        # Create initial note
        note = Note(
            complaint_id=complaint.id,
            content='Complaint created',
            note_type='system'
        )
        db.session.add(note)

        # Create deadline reminders
        if filing_deadline:
            reminders = calculate_reminder_dates(filing_deadline)
            for reminder_data in reminders:
                reminder = Reminder(
                    user_id=current_user.id,
                    complaint_id=complaint.id,
                    reminder_date=datetime.combine(reminder_data['date'], datetime.min.time()),
                    reminder_type='filing_deadline',
                    message=f"{complaint.title}: {reminder_data['message']}"
                )
                db.session.add(reminder)

        db.session.commit()

        flash('Complaint created successfully!', 'success')
        return redirect(url_for('view_complaint', complaint_id=complaint.id))

    # GET request - show form
    jurisdiction = session.get('jurisdiction', {})
    nar_articles = get_articles_list()
    states = get_all_states()

    return render_template('complaint_form.html',
                         jurisdiction=jurisdiction,
                         nar_articles=nar_articles,
                         states=states)


@app.route('/complaint/<int:complaint_id>')
@login_required
def view_complaint(complaint_id):
    """View complaint details"""
    complaint = Complaint.query.get_or_404(complaint_id)

    # Check ownership
    if complaint.user_id != current_user.id:
        flash('You do not have permission to view this complaint.', 'danger')
        return redirect(url_for('dashboard'))

    # Get deadline status
    deadline_info = get_deadline_status(complaint.filing_deadline) if complaint.filing_deadline else None

    # Get required documents checklist
    required_docs = get_required_documents(complaint.state, complaint.jurisdiction_type)
    filing_checklist = get_filing_checklist(complaint.state, complaint.jurisdiction_type)

    # Get state/jurisdiction info
    if complaint.jurisdiction_type == 'nar_association':
        jurisdiction_info = get_nar_requirements()
    elif complaint.state:
        jurisdiction_info = get_state_requirements(complaint.state)
    else:
        jurisdiction_info = None

    # Parse alleged violations
    alleged_violations = []
    if complaint.alleged_violations:
        article_numbers = json.loads(complaint.alleged_violations)
        for article_num in article_numbers:
            article = get_article(article_num)
            if article:
                alleged_violations.append({
                    'number': article_num,
                    'data': article
                })

    return render_template('complaint_detail.html',
                         complaint=complaint,
                         deadline_info=deadline_info,
                         required_docs=required_docs,
                         filing_checklist=filing_checklist,
                         jurisdiction_info=jurisdiction_info,
                         alleged_violations=alleged_violations)


@app.route('/complaint/<int:complaint_id>/upload', methods=['GET', 'POST'])
@login_required
def upload_document(complaint_id):
    """Upload documents for a complaint"""
    complaint = Complaint.query.get_or_404(complaint_id)

    if complaint.user_id != current_user.id:
        flash('You do not have permission to upload documents to this complaint.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'warning')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No file selected', 'warning')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Create unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_filename = f"{complaint.id}_{timestamp}_{filename}"

            # Ensure upload directory exists
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)

            # Create document record
            document = Document(
                complaint_id=complaint.id,
                filename=unique_filename,
                original_filename=filename,
                file_path=file_path,
                file_type=request.form.get('file_type'),
                file_size=os.path.getsize(file_path),
                description=request.form.get('description')
            )

            db.session.add(document)

            # Add note
            note = Note(
                complaint_id=complaint.id,
                content=f'Document uploaded: {filename}',
                note_type='system'
            )
            db.session.add(note)

            db.session.commit()

            flash('Document uploaded successfully!', 'success')
            return redirect(url_for('view_complaint', complaint_id=complaint.id))
        else:
            flash('File type not allowed', 'danger')

    return render_template('document_upload.html', complaint=complaint)


@app.route('/complaint/<int:complaint_id>/note', methods=['POST'])
@login_required
def add_note(complaint_id):
    """Add a note to a complaint"""
    complaint = Complaint.query.get_or_404(complaint_id)

    if complaint.user_id != current_user.id:
        flash('You do not have permission to add notes to this complaint.', 'danger')
        return redirect(url_for('dashboard'))

    content = request.form.get('content')
    if content:
        note = Note(
            complaint_id=complaint.id,
            content=content,
            note_type='user'
        )
        db.session.add(note)
        db.session.commit()
        flash('Note added successfully!', 'success')

    return redirect(url_for('view_complaint', complaint_id=complaint.id))


@app.route('/education')
def education():
    """Educational resources page"""
    nar_articles = get_all_articles()
    return render_template('education.html', nar_articles=nar_articles)


@app.route('/api/nar-articles')
def api_nar_articles():
    """API endpoint for NAR articles"""
    search_term = request.args.get('q', '')
    if search_term:
        results = search_articles(search_term)
        return jsonify(results)
    return jsonify(get_all_articles())


@app.route('/api/deadline-calculator', methods=['POST'])
def api_deadline_calculator():
    """API endpoint for deadline calculation"""
    data = request.json
    incident_date = datetime.strptime(data['incident_date'], '%Y-%m-%d').date()
    jurisdiction_type = data['jurisdiction_type']
    state = data.get('state')

    deadline = calculate_filing_deadline(incident_date, jurisdiction_type, state)
    days_left = days_until_deadline(deadline)
    status = get_deadline_status(deadline)

    return jsonify({
        'deadline': deadline.isoformat(),
        'days_remaining': days_left,
        'status': status
    })


# Initialize database
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    # Use port from environment variable for production, or 3000 for local development
    import os
    port = int(os.environ.get('PORT', 3000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)
