# Grievance Filing Service - Application Flow

## User Journey Map

```
┌─────────────────────────────────────────────────────────────────────┐
│                         HOMEPAGE (/)                                 │
│  - Overview of features                                             │
│  - Call to action: Register or Learn More                           │
└─────────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
         ┌──────────────────┐   ┌──────────────────┐
         │  REGISTER (/register) │  LOGIN (/login)  │
         │  - Create account     │  - Authenticate  │
         │  - Select user type   │                  │
         └──────────────────┘   └──────────────────┘
                    │                   │
                    └─────────┬─────────┘
                              ▼
         ┌──────────────────────────────────────────┐
         │        DASHBOARD (/dashboard)            │
         │  - View all complaints                   │
         │  - Track deadlines                       │
         │  - See statistics                        │
         │  - Quick access to actions               │
         └──────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
         ┌──────────────────┐   ┌──────────────────┐
         │ NEW COMPLAINT    │   │ VIEW EXISTING    │
         │                  │   │ COMPLAINT        │
         └──────────────────┘   └──────────────────┘
                    │                   │
                    ▼                   │
         ┌──────────────────────────────────────────┐
         │  JURISDICTION SCREENING                  │
         │  (/jurisdiction-screening)               │
         │  - Answer 5 key questions                │
         │  - Determine filing location             │
         │  - Get recommendations                   │
         └──────────────────────────────────────────┘
                              │
                              ▼
         ┌──────────────────────────────────────────┐
         │  COMPLAINT FORM (/complaint/new)         │
         │  - Basic information                     │
         │  - Respondent details                    │
         │  - Incident information                  │
         │  - Narrative                             │
         │  - NAR Code violations (if applicable)   │
         └──────────────────────────────────────────┘
                              │
                              ▼
         ┌──────────────────────────────────────────┐
         │  COMPLAINT CREATED                       │
         │  - Deadline calculated                   │
         │  - Reminders scheduled                   │
         │  - Status: Draft                         │
         └──────────────────────────────────────────┘
                              │
                              ▼
         ┌──────────────────────────────────────────┐
         │  COMPLAINT DETAIL VIEW                   │
         │  (/complaint/<id>)                       │
         │  - View all information                  │
         │  - See deadline status                   │
         │  - Upload documents                      │
         │  - Add notes                             │
         │  - Track progress                        │
         └──────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
         ┌──────────────────┐   ┌──────────────────┐
         │ UPLOAD DOCUMENTS │   │  ADD NOTES       │
         │ (/complaint/<id>/│   │  (/complaint/<id>│
         │  upload)         │   │   /note)         │
         │  - Select file   │   │  - Track updates │
         │  - Categorize    │   │  - Timeline      │
         │  - Describe      │   │                  │
         └──────────────────┘   └──────────────────┘
                    │                   │
                    └─────────┬─────────┘
                              ▼
         ┌──────────────────────────────────────────┐
         │  READY TO SUBMIT                         │
         │  - All documents uploaded                │
         │  - Checklist complete                    │
         │  - Narrative finalized                   │
         │  - Submit to appropriate agency          │
         └──────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌──────────────┐
│    User      │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────┐
│         Flask Application                │
│  ┌────────────────────────────────────┐  │
│  │  Routes (app.py)                   │  │
│  │  - Authentication                  │  │
│  │  - Complaint Management            │  │
│  │  - Document Upload                 │  │
│  │  - Dashboard                       │  │
│  └─────────────┬──────────────────────┘  │
│                │                          │
│  ┌─────────────▼──────────────────────┐  │
│  │  Business Logic (utils/)           │  │
│  │  - Deadline Calculator             │  │
│  │  - NAR Code Articles               │  │
│  │  - State Requirements              │  │
│  └─────────────┬──────────────────────┘  │
│                │                          │
│  ┌─────────────▼──────────────────────┐  │
│  │  Database Models (models.py)       │  │
│  │  - User                            │  │
│  │  - Complaint                       │  │
│  │  - Document                        │  │
│  │  - Note                            │  │
│  │  - Reminder                        │  │
│  └─────────────┬──────────────────────┘  │
└────────────────┼──────────────────────────┘
                 │
                 ▼
         ┌───────────────┐
         │  SQLite DB    │
         │  (database.db)│
         └───────────────┘
                 │
                 ▼
         ┌───────────────┐
         │  File Storage │
         │  (static/     │
         │   uploads/)   │
         └───────────────┘
```

## Feature Interaction Map

```
                    ┌─────────────────────┐
                    │  User Dashboard     │
                    └──────────┬──────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
         ▼                     ▼                     ▼
┌────────────────┐   ┌────────────────┐   ┌────────────────┐
│ Jurisdiction   │   │ Complaint      │   │  Education     │
│ Screening      │   │ Management     │   │  Resources     │
└────────┬───────┘   └────────┬───────┘   └────────────────┘
         │                     │
         │  Recommends         │
         │  Jurisdiction       │
         └─────────┬───────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │  Complaint Form     │
         └──────────┬──────────┘
                    │
         ┌──────────┼──────────┐
         │          │          │
         ▼          ▼          ▼
┌────────────┐ ┌────────┐ ┌────────────┐
│ Deadline   │ │ NAR    │ │  State     │
│ Calculator │ │ Code   │ │  Forms     │
└────────┬───┘ └───┬────┘ └─────┬──────┘
         │         │            │
         └─────────┼────────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │  Database Storage   │
         └─────────────────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │  Reminder System    │
         │  (Future: Email)    │
         └─────────────────────┘
```

## Deadline Tracking Flow

```
Incident Date
     │
     ▼
┌─────────────────────────────┐
│ Calculate Filing Deadline   │
│ Based on:                   │
│ - Jurisdiction Type         │
│ - State                     │
│ - Incident Date             │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Generate Reminders          │
│ - 90 days before            │
│ - 30 days before            │
│ - 7 days before             │
│ - 1 day before              │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Display Status              │
│ - Sufficient Time (green)   │
│ - Upcoming (blue)           │
│ - Approaching (yellow)      │
│ - Urgent (orange)           │
│ - Expired (red)             │
└─────────────────────────────┘
```

## Document Upload Flow

```
User selects file
     │
     ▼
┌─────────────────────────────┐
│ Validate File               │
│ - Check extension           │
│ - Check size (max 16MB)     │
│ - Sanitize filename         │
└─────────────┬───────────────┘
              │
         Valid? ├─ No ──> Error message
              │
             Yes
              ▼
┌─────────────────────────────┐
│ Generate Unique Filename    │
│ Format: <complaint_id>_     │
│         <timestamp>_        │
│         <original_name>     │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Save to Storage             │
│ Path: static/uploads/       │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Create Document Record      │
│ - complaint_id              │
│ - filename                  │
│ - file_type                 │
│ - file_size                 │
│ - description               │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Add System Note             │
│ "Document uploaded: <name>" │
└─────────────┬───────────────┘
              │
              ▼
    Success confirmation
```

## Jurisdiction Decision Tree

```
Start Screening
     │
     ▼
Is respondent a REALTOR®?
     │
     ├─ Yes ──> What's the violation type?
     │            │
     │            ├─ Ethics Violation ──────┐
     │            │                         │
     │            └─ License Violation ──┐  │
     │                                   │  │
     └─ No ───> License Violation ──────┤  │
                                        │  │
Seeks monetary damages? ◄──────────────┘  │
     │                                     │
     ├─ Yes ──> Civil Court ──────────────┼──> Recommendation
     │                                     │
     └─ No ──> State Board ◄──────────────┤
                    ▲                      │
                    │                      │
                    └──────────────────────┘
                                           │
                                           ▼
                              NAR/Local Association
```

## Security Flow

```
User Request
     │
     ▼
┌─────────────────────────────┐
│ Flask Application           │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Authentication Check        │
│ (Flask-Login)               │
└─────────────┬───────────────┘
              │
         Authenticated?
              │
         ┌────┴────┐
        No         Yes
         │          │
         ▼          ▼
    Redirect   ┌─────────────────────────────┐
    to Login   │ Authorization Check         │
               │ - Owns complaint?           │
               └─────────────┬───────────────┘
                             │
                        Authorized?
                             │
                        ┌────┴────┐
                       No         Yes
                        │          │
                        ▼          ▼
                   403 Error   ┌─────────────────────────────┐
                               │ Input Validation            │
                               │ - CSRF Token (Flask-WTF)    │
                               │ - SQL Injection (ORM)       │
                               │ - File Upload Validation    │
                               └─────────────┬───────────────┘
                                             │
                                             ▼
                                    Process Request
```

## Database Relationships

```
┌──────────────┐
│    User      │
│  (id: PK)    │
└──────┬───────┘
       │ 1
       │
       │ *
       ▼
┌──────────────────┐          ┌──────────────┐
│   Complaint      │ 1     *  │  Document    │
│   (id: PK)       ├──────────┤  (id: PK)    │
│   (user_id: FK)  │          │  (complaint_ │
└────┬─────────┬───┘          │   id: FK)    │
     │ 1       │ 1            └──────────────┘
     │         │
     │ *       │ *
     ▼         ▼
┌──────────┐  ┌──────────┐
│   Note   │  │ Reminder │
│ (id: PK) │  │ (id: PK) │
│(complaint│  │(user_id: │
│ _id: FK) │  │   FK)    │
└──────────┘  │(complaint│
              │ _id: FK) │
              └──────────┘
```

## State & Jurisdiction Coverage

```
Supported States
├── Florida (FL)
│   ├── Agency: FL DBPR
│   ├── Deadline: 2 years
│   ├── Special: 10-day confidentiality
│   └── Required: Front/back of checks
│
├── Kentucky (KY)
│   ├── Agency: KREC
│   ├── Deadline: 1 year
│   ├── Special: Notarization required
│   └── Form: KREC Form 300
│
├── Colorado (CO)
│   ├── Agency: Division of Real Estate
│   ├── Deadline: 1 year
│   └── Investigation: 240 days target
│
├── California (CA)
│   ├── Agency: CA DRE
│   └── Deadline: 3 years
│
└── Texas (TX)
    ├── Agency: TREC
    └── Deadline: 2 years

NAR Association
├── Filing: Local REALTOR® Association
├── Deadline: 180 days from offense
├── Process: Grievance → Mediation → Hearing
└── Scope: Ethics violations only
```

---

This application flow demonstrates a comprehensive, well-structured system that guides users through every step of the grievance filing process while maintaining security, organization, and ease of use.
