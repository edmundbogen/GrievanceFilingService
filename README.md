# Grievance Filing Service

A comprehensive web application designed to assist consumers and REALTORS® in filing complaints and grievances against real estate professionals.

## Overview

The Grievance Filing Service guides users through the complex process of filing complaints with state licensing boards, NAR/local REALTOR® associations, or civil courts. The application provides:

- Jurisdiction screening to determine proper filing location
- Automated deadline tracking and reminders
- Document organization and upload system
- Complaint drafting assistance with NAR Code of Ethics reference
- Status tracking dashboard
- Educational resources about ethics violations and filing processes

## Features

### 1. Jurisdiction Screening & Guidance
- Interactive questionnaire to determine whether complaints should be filed with:
  - State licensing boards (license law violations)
  - REALTOR® associations (ethics violations)
  - Civil court (contract disputes)
- Automatic verification of respondent status

### 2. Deadline Tracking & Reminders
- Automatic calculation of filing deadlines based on jurisdiction:
  - NAR Ethics: 180 days after offense
  - State boards: Varies by state (365-1095 days)
- Automated reminder system at 90, 30, 7, and 1 day before deadline
- Visual deadline status indicators

### 3. Document Collection & Organization
- Secure document upload portal
- Support for multiple file types (PDF, DOCX, DOC, JPG, PNG, TXT)
- Document categorization (contracts, checks, correspondence, etc.)
- Jurisdiction-specific checklists for required documents

### 4. Complaint Drafting Assistant
- Templates for clear, effective complaints
- NAR Code of Ethics article selection with plain-language summaries
- Guided narrative structure
- Form auto-population with user data

### 5. Status Tracking Dashboard
- View all complaints in one place
- Track complaint status (draft, submitted, under review, closed)
- Monitor deadlines and investigation timelines
- Add notes and updates

### 6. Educational Resources
- Comprehensive NAR Code of Ethics reference
- Explanation of all 17 Articles with common violations
- Filing process guidance
- Timeline expectations
- Best practices

## Technology Stack

- **Backend**: Python 3.6+ with Flask
- **Database**: SQLite (easily upgradeable to PostgreSQL)
- **Authentication**: Flask-Login
- **Frontend**: Bootstrap 5, HTML/CSS/JavaScript
- **File Storage**: Local filesystem (expandable to cloud storage)
- **Task Scheduling**: APScheduler (for reminders)

## Installation

### Prerequisites
- Python 3.6 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or navigate to the project directory**:
   ```bash
   cd GrievanceFilingService
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables** (optional):
   Create a `.env` file in the project root:
   ```
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///database.db
   ```

5. **Initialize the database**:
   The database will be automatically created when you first run the application.

6. **Run the application**:
   ```bash
   python3 app.py
   ```

7. **Access the application**:
   Open your browser and navigate to: `http://localhost:5000`

## Usage Guide

### For Consumers and REALTORS®

1. **Register an Account**
   - Visit the registration page
   - Provide your name, email, and select user type (Consumer or REALTOR®)

2. **File a New Complaint**
   - Complete the jurisdiction screening questionnaire
   - Fill out the complaint form with incident details
   - Upload supporting documents
   - Submit when ready

3. **Track Your Complaints**
   - View all complaints on your dashboard
   - Monitor filing deadlines
   - Add notes and updates
   - Upload additional documents as needed

4. **Learn About the Process**
   - Visit the Education page for NAR Code of Ethics information
   - Review filing requirements for your jurisdiction
   - Understand timeline expectations

## Project Structure

```
GrievanceFilingService/
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── models.py                       # Database models
├── requirements.txt                # Python dependencies
├── database.db                     # SQLite database (created on first run)
├── README.md                       # This file
├── templates/                      # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── jurisdiction_screening.html
│   ├── complaint_form.html
│   ├── complaint_detail.html
│   ├── document_upload.html
│   └── education.html
├── static/                         # Static files
│   ├── css/
│   ├── js/
│   └── uploads/                    # User-uploaded documents
└── utils/                          # Helper modules
    ├── deadline_calculator.py      # Deadline calculation utilities
    ├── nar_code_articles.py        # NAR Code of Ethics data
    └── state_forms.py              # State-specific requirements
```

## Database Schema

### User
- User authentication and profile information
- Tracks all user complaints

### Complaint
- Core complaint details (respondent, incident, narrative)
- Jurisdiction and deadline tracking
- Status management

### Document
- File uploads linked to complaints
- Metadata (type, size, description)

### Note
- User notes and system updates
- Timeline of complaint activity

### Reminder
- Automated deadline reminders
- Email notification preparation (future feature)

## Key Features by Jurisdiction

### State Licensing Boards
- Florida: 2-year deadline, 10-day confidentiality period
- Kentucky: 1-year deadline, notarization required
- Colorado: 1-year deadline, 240-day investigation target
- California: 3-year deadline
- Texas: 2-year deadline

### NAR Association Ethics
- 180-day deadline from offense or transaction close
- Must cite specific Code of Ethics articles
- Filed with local REALTOR® association
- Ombudsman/mediation services available

## Important Disclaimers

1. **Not Legal Advice**: This service provides guidance for filing grievances but does not constitute legal advice. Consult a licensed attorney for legal matters.

2. **Administrative Process**: Grievance processes are administrative and cannot:
   - Award monetary damages
   - Enforce contracts
   - Provide compensation

3. **Legal Matters**: For contract enforcement or monetary damages, users should consult with a licensed attorney or file in civil court.

## Future Enhancements

- [ ] Email notification system for deadline reminders
- [ ] License verification API integration
- [ ] PDF form generation and auto-population
- [ ] Cloud storage integration (AWS S3, Google Cloud)
- [ ] Advanced search and filtering
- [ ] Export complaint summaries to PDF
- [ ] Multi-language support
- [ ] Mobile app version
- [ ] Integration with state board submission portals

## Security Considerations

- Passwords are hashed using Werkzeug's security functions
- File uploads are validated and sanitized
- SQL injection protection via SQLAlchemy ORM
- CSRF protection via Flask-WTF
- Session security with configurable timeouts

## Support

For questions or issues:
- Review the Education page for general guidance
- Check state-specific requirements in the app
- Consult with an attorney for legal matters

## License

This project is designed for use by Edmund Bogen and related real estate service businesses.

## Credits

Developed to assist consumers and REALTORS® in navigating the complex grievance filing process across multiple jurisdictions.

---

**Last Updated**: 2025
**Version**: 1.0.0
