"""
Deadline calculation utilities for grievance filing
"""
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def calculate_filing_deadline(incident_date, jurisdiction_type, state=None):
    """
    Calculate the filing deadline based on jurisdiction and incident date

    Args:
        incident_date: datetime.date object of when the incident occurred
        jurisdiction_type: str - 'state_board', 'nar_association', 'civil_court'
        state: str - state abbreviation (e.g., 'FL', 'KY', 'CO')

    Returns:
        datetime.date object representing the filing deadline
    """
    if not incident_date:
        return None

    if isinstance(incident_date, str):
        incident_date = datetime.strptime(incident_date, '%Y-%m-%d').date()

    # Default deadlines in days
    deadline_days = {
        'nar_association': 180,  # NAR ethics complaints: 180 days
        'state_board': 365,      # Most state boards: 1 year
        'civil_court': 730       # Civil matters vary, 2 years is common
    }

    # State-specific overrides
    state_specific_deadlines = {
        'KY': 365,   # Kentucky: 1 year
        'FL': 730,   # Florida: 2 years (example)
        'CO': 365,   # Colorado: 1 year
        'CA': 1095   # California: 3 years (example)
    }

    # Determine applicable deadline
    if state and state.upper() in state_specific_deadlines:
        days_to_add = state_specific_deadlines[state.upper()]
    else:
        days_to_add = deadline_days.get(jurisdiction_type, 180)

    deadline = incident_date + timedelta(days=days_to_add)
    return deadline


def calculate_reminder_dates(filing_deadline):
    """
    Calculate reminder dates before the filing deadline

    Returns list of reminder dates:
    - 90 days before deadline
    - 30 days before deadline
    - 7 days before deadline
    - 1 day before deadline
    """
    if not filing_deadline:
        return []

    if isinstance(filing_deadline, str):
        filing_deadline = datetime.strptime(filing_deadline, '%Y-%m-%d').date()

    reminders = []
    reminder_intervals = [90, 30, 7, 1]  # days before deadline

    for days_before in reminder_intervals:
        reminder_date = filing_deadline - timedelta(days=days_before)
        if reminder_date > datetime.now().date():  # Only future reminders
            reminders.append({
                'date': reminder_date,
                'days_before': days_before,
                'message': f"Filing deadline in {days_before} day{'s' if days_before > 1 else ''}"
            })

    return reminders


def days_until_deadline(deadline_date):
    """Calculate days remaining until deadline"""
    if not deadline_date:
        return None

    if isinstance(deadline_date, str):
        deadline_date = datetime.strptime(deadline_date, '%Y-%m-%d').date()

    today = datetime.now().date()
    delta = deadline_date - today

    return delta.days


def is_deadline_passed(deadline_date):
    """Check if deadline has passed"""
    if not deadline_date:
        return False

    days_left = days_until_deadline(deadline_date)
    return days_left < 0 if days_left is not None else False


def estimate_investigation_completion(submission_date, state=None):
    """
    Estimate when investigation might complete

    Args:
        submission_date: date when complaint was submitted
        state: state abbreviation

    Returns:
        Estimated completion date
    """
    if not submission_date:
        return None

    if isinstance(submission_date, str):
        submission_date = datetime.strptime(submission_date, '%Y-%m-%d').date()

    # Investigation timelines in days
    investigation_timelines = {
        'CO': 240,    # Colorado aims for 240 days
        'DEFAULT': 180  # Default estimate
    }

    days_to_add = investigation_timelines.get(
        state.upper() if state else 'DEFAULT',
        investigation_timelines['DEFAULT']
    )

    completion_date = submission_date + timedelta(days=days_to_add)
    return completion_date


def get_deadline_status(deadline_date):
    """
    Get status and urgency level of deadline

    Returns dict with status, urgency, and message
    """
    if not deadline_date:
        return {
            'status': 'unknown',
            'urgency': 'none',
            'message': 'No deadline set'
        }

    days_left = days_until_deadline(deadline_date)

    if days_left < 0:
        return {
            'status': 'expired',
            'urgency': 'critical',
            'message': f'Deadline passed {abs(days_left)} days ago',
            'css_class': 'danger'
        }
    elif days_left <= 7:
        return {
            'status': 'urgent',
            'urgency': 'high',
            'message': f'{days_left} days remaining - File immediately!',
            'css_class': 'danger'
        }
    elif days_left <= 30:
        return {
            'status': 'approaching',
            'urgency': 'medium',
            'message': f'{days_left} days remaining - Begin preparation',
            'css_class': 'warning'
        }
    elif days_left <= 90:
        return {
            'status': 'upcoming',
            'urgency': 'low',
            'message': f'{days_left} days remaining',
            'css_class': 'info'
        }
    else:
        return {
            'status': 'sufficient_time',
            'urgency': 'none',
            'message': f'{days_left} days remaining',
            'css_class': 'success'
        }
