# Coffee-Chat-Generator

Generate personalized coffee-chat outreach emails from your resume and a few inputs, then preview, schedule, and optionally send them. The project also includes a lightweight web UI.

## What it does

- Drafts outreach emails using your details and targets you provide (role, company, person, context). Utilizes Groq API for LLM based email generation.
- Parses your resume to auto-pull highlights and talking points (via `ResumeParser/`).
- Integrates with Gmail to create drafts or send emails (via `GmailAPI.py` and `EmailSend.py`).
- Checks calendar availability for proposing times (via `GoogleCalendarAPI/` and `GCal_credentials.json`).
- Provides a simple web app to generate and copy emails quickly (`website.py` and `app/`).

## Quickstart

### 1) Prerequisites
- Python 3.9+ recommended
- A Google Cloud project with Gmail and Calendar APIs enabled (if you plan to use send/draft or availability features)
- A resume file (PDF or DOCX) if you want auto-parsed highlights
- A test Gmail account or OAuth client for development

### 2) Clone and install

git clone https://github.com/rab547/Coffee-Chat-Generator.git
cd Coffee-Chat-Generator
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt


### 3) Configure Credentials

# credentials.py (example)
GMAIL_SENDER = "your_address@gmail.com"

