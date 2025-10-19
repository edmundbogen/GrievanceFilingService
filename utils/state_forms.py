"""
State-specific form requirements and checklists
"""

STATE_REQUIREMENTS = {
    'FL': {
        'name': 'Florida',
        'agency': 'Florida Department of Business and Professional Regulation (DBPR)',
        'form_name': 'DBPR Complaint Form',
        'website': 'https://www.myfloridalicense.com/dbpr/re/',
        'filing_deadline_days': 730,  # 2 years
        'confidentiality_period_days': 10,
        'required_documents': [
            'Front and back copies of all checks',
            'Complete sales contract',
            'All written correspondence',
            'Listing agreement (if applicable)',
            'Inspection reports (if relevant)'
        ],
        'checklist': [
            'Verify respondent\'s license number via DBPR website',
            'Gather all transaction documents',
            'Copy all checks (front and back)',
            'Organize correspondence chronologically',
            'Write detailed chronological narrative',
            'Complete DBPR complaint form',
            'Submit online or mail to DBPR'
        ],
        'notes': [
            'Florida has a 10-day confidentiality period after filing',
            'DBPR cannot award money or enforce contracts',
            'Process is administrative, not civil'
        ],
        'contact': {
            'phone': '850-487-1395',
            'email': 'DBPR.CustomerService@myfloridalicense.com'
        }
    },
    'KY': {
        'name': 'Kentucky',
        'agency': 'Kentucky Real Estate Commission (KREC)',
        'form_name': 'KREC Form 300 - Complaint Form',
        'website': 'https://krec.ky.gov/',
        'filing_deadline_days': 365,  # 1 year
        'notarization_required': True,
        'required_documents': [
            'Completed KREC Form 300',
            'Notarized signature',
            'Supporting documentation',
            'Contract copies',
            'Correspondence'
        ],
        'checklist': [
            'Download KREC Form 300',
            'Verify respondent\'s license status',
            'Complete all sections of Form 300',
            'Attach supporting documents',
            'Get signature notarized',
            'Mail to KREC office',
            'Keep copies for records'
        ],
        'notes': [
            'Complaint must be notarized',
            'KREC investigates license law violations',
            'Mediation services may be available'
        ],
        'contact': {
            'phone': '502-429-7250',
            'address': '2365 Harrodsburg Road, Suite B-340, Lexington, KY 40504'
        }
    },
    'CO': {
        'name': 'Colorado',
        'agency': 'Colorado Division of Real Estate',
        'form_name': 'Division of Real Estate Complaint Form',
        'website': 'https://dre.colorado.gov/',
        'filing_deadline_days': 365,
        'investigation_timeline_days': 240,  # Aims for 240 days
        'required_documents': [
            'Completed complaint form',
            'All supporting documentation',
            'Contracts',
            'Correspondence',
            'Evidence of violation'
        ],
        'checklist': [
            'Verify license through DORA website',
            'Complete online or paper complaint form',
            'Attach all supporting documents',
            'Provide detailed timeline of events',
            'Submit via mail or online portal',
            'Track complaint status online'
        ],
        'notes': [
            'Colorado aims to complete investigations within 240 days',
            'Complaint must relate to license law violations',
            'Ombudsman services available for informal resolution'
        ],
        'contact': {
            'phone': '303-894-2166',
            'email': 'dre@state.co.us'
        }
    },
    'CA': {
        'name': 'California',
        'agency': 'California Department of Real Estate (DRE)',
        'form_name': 'DRE Complaint Form',
        'website': 'https://dre.ca.gov/',
        'filing_deadline_days': 1095,  # 3 years typical
        'required_documents': [
            'Detailed written complaint',
            'Names and addresses of all parties',
            'Dates and locations of incidents',
            'Supporting documents',
            'Witness information'
        ],
        'checklist': [
            'Verify license on DRE website',
            'Document names, dates, locations',
            'List all witnesses',
            'Gather supporting documents',
            'Write chronological narrative',
            'Submit complaint to local DRE office',
            'Keep complaint reference number'
        ],
        'notes': [
            'DRE cannot award money or enforce contracts',
            'Process is administrative',
            'Consider consulting attorney for civil matters'
        ],
        'contact': {
            'phone': '877-373-4542',
            'website': 'https://dre.ca.gov/Consumers/FileComplaint.html'
        }
    },
    'TX': {
        'name': 'Texas',
        'agency': 'Texas Real Estate Commission (TREC)',
        'form_name': 'TREC Complaint Form',
        'website': 'https://www.trec.texas.gov/',
        'filing_deadline_days': 730,
        'required_documents': [
            'TREC complaint form',
            'Supporting documentation',
            'Contracts and agreements',
            'Correspondence',
            'Evidence of violations'
        ],
        'checklist': [
            'Verify license on TREC website',
            'Complete TREC complaint form',
            'Attach all relevant documents',
            'Provide detailed description',
            'Submit online or by mail',
            'Note complaint number for tracking'
        ],
        'notes': [
            'TREC investigates license law violations',
            'Cannot resolve contract disputes',
            'Mediation available through local associations'
        ],
        'contact': {
            'phone': '512-936-3000',
            'email': 'trec@trec.texas.gov'
        }
    }
}

# NAR Association requirements (separate from state boards)
NAR_REQUIREMENTS = {
    'name': 'National Association of REALTORS® (NAR)',
    'type': 'Ethics Complaint',
    'filing_deadline_days': 180,  # 180 days after offense or transaction close
    'filed_with': 'Local REALTOR® Association',
    'required_elements': [
        'Respondent must be a REALTOR® member',
        'Complaint must cite specific Code of Ethics articles',
        'Must be filed with appropriate local association',
        'Written complaint with supporting documentation',
        'Identification of all parties involved'
    ],
    'process_steps': [
        'Contact local REALTOR® association',
        'Verify respondent is NAR member',
        'Identify alleged Code violations',
        'Gather supporting documentation',
        'File written complaint with association',
        'Grievance committee reviews',
        'Possible mediation or ombudsman',
        'Professional standards hearing (if warranted)'
    ],
    'notes': [
        'Complaint must be filed within 180 days of offense or transaction closing',
        'Can only discipline NAR members',
        'Ombudsman services often available for informal resolution',
        'Process is confidential',
        'Cannot award monetary damages',
        'May result in education, warning, fine, or membership suspension/termination'
    ],
    'find_local_association': 'https://www.nar.realtor/about-nar/governing-documents/the-code-of-ethics'
}


def get_state_requirements(state_code):
    """Get requirements for specific state"""
    return STATE_REQUIREMENTS.get(state_code.upper())


def get_nar_requirements():
    """Get NAR ethics complaint requirements"""
    return NAR_REQUIREMENTS


def get_all_states():
    """Get list of all states with requirements"""
    return [
        {'code': code, 'name': data['name']}
        for code, data in STATE_REQUIREMENTS.items()
    ]


def get_required_documents(state_code=None, jurisdiction_type='state_board'):
    """Get checklist of required documents"""
    if jurisdiction_type == 'nar_association':
        return NAR_REQUIREMENTS['required_elements']

    if state_code and state_code.upper() in STATE_REQUIREMENTS:
        return STATE_REQUIREMENTS[state_code.upper()]['required_documents']

    # Default generic requirements
    return [
        'Written complaint narrative',
        'All contracts and agreements',
        'Correspondence with respondent',
        'Supporting documentation',
        'Evidence of violation',
        'Witness information (if applicable)'
    ]


def get_filing_checklist(state_code=None, jurisdiction_type='state_board'):
    """Get step-by-step filing checklist"""
    if jurisdiction_type == 'nar_association':
        return NAR_REQUIREMENTS['process_steps']

    if state_code and state_code.upper() in STATE_REQUIREMENTS:
        return STATE_REQUIREMENTS[state_code.upper()]['checklist']

    # Default generic checklist
    return [
        'Verify respondent license/membership status',
        'Determine appropriate filing jurisdiction',
        'Calculate filing deadline',
        'Gather all required documentation',
        'Write detailed chronological narrative',
        'Complete required forms',
        'Submit complaint to appropriate agency',
        'Retain copies and reference numbers'
    ]
