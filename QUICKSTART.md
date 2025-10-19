# Quick Start Guide - Grievance Filing Service

## Getting Started in 5 Minutes

### Step 1: Navigate to the Project
```bash
cd /Users/edmundbogen/GrievanceFilingService
```

### Step 2: Activate Virtual Environment
```bash
source venv/bin/activate
```

### Step 3: Run the Application
```bash
python3 app.py
```

### Step 4: Open in Browser
Open your web browser and go to:
```
http://localhost:5000
```

## First Time Setup (Already Done!)

The following has already been completed:
- ✅ Virtual environment created
- ✅ Dependencies installed
- ✅ Database initialized

## Using the Application

### Register a New Account
1. Click "Register" in the navigation bar
2. Fill out the form with your information
3. Select user type (Consumer or REALTOR®)
4. Click "Create Account"

### File Your First Complaint

1. **Login** with your credentials

2. **Start Jurisdiction Screening**
   - Click "New Complaint" or "File New Complaint"
   - Answer the screening questions
   - The system will recommend the appropriate filing jurisdiction

3. **Fill Out Complaint Form**
   - Enter respondent information (name, license number, brokerage)
   - Provide incident details (date, location, transaction type)
   - Write your complaint narrative (be specific and chronological)
   - Select NAR Code of Ethics violations (if applicable)
   - Click "Create Complaint"

4. **Upload Documents**
   - From your complaint detail page, click "Upload"
   - Select document type (contract, check, correspondence, etc.)
   - Choose your file
   - Add a description
   - Click "Upload Document"

5. **Track Progress**
   - View all complaints on your dashboard
   - Monitor filing deadlines
   - Add notes and updates
   - Check required documents checklist

## Key Features to Explore

### Dashboard
- View all your complaints at a glance
- See filing deadline status
- Track complaint statuses

### Education Page
- Learn about NAR Code of Ethics
- Understand filing requirements
- Review process timelines
- Get best practice tips

### Complaint Detail Page
- View complete complaint information
- See jurisdiction-specific requirements
- Track uploaded documents
- Add notes and updates
- Monitor deadline status

## Sample Workflow

Here's a typical workflow for filing a complaint:

1. **Day 1**: Create account, complete jurisdiction screening
2. **Day 2-3**: Gather all documents (contracts, emails, checks)
3. **Day 4**: Fill out complaint form with detailed narrative
4. **Day 5**: Upload all supporting documents
5. **Day 6**: Review checklist and ensure all requirements met
6. **Day 7**: Submit complaint to appropriate agency
5. **Ongoing**: Monitor deadline reminders and add status updates

## Stopping the Application

Press `CTRL+C` in the terminal where the app is running

Or if running in background:
```bash
pkill -f "python3 app.py"
```

## Troubleshooting

### Port Already in Use
If you see "Address already in use", kill the existing process:
```bash
lsof -ti:5000 | xargs kill -9
```

### Database Issues
If you need to reset the database:
```bash
rm database.db
python3 app.py  # Will recreate the database
```

### Dependencies Issues
Reinstall dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Important Reminders

- **This is NOT legal advice** - Consult an attorney for legal matters
- **Administrative only** - State boards and associations cannot award money
- **Deadlines are critical** - Watch your filing deadlines carefully
- **Documentation is key** - Upload all relevant supporting documents
- **Keep copies** - Always maintain your own records

## Next Steps

1. **Customize** - Update state requirements in `utils/state_forms.py`
2. **Enhance** - Add more states and jurisdictions
3. **Deploy** - Consider deploying to a production server
4. **Secure** - Update `SECRET_KEY` in production

## Support

For questions about:
- **The application**: Check README.md and documentation
- **Legal matters**: Consult a licensed attorney
- **Filing process**: Visit the Education page in the app
- **State requirements**: Check your state's real estate commission website

---

**Ready to start?** Run `python3 app.py` and visit http://localhost:5000

Happy filing!
