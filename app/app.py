# Import necessary modules
import pyrebase
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from datetime import datetime
import re
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
import pathlib
import os
from google.oauth2 import id_token
import firebase as fire
import json
from PyPDF2 import PdfReader
from google.auth.transport.requests import Request
import sys
from pathlib import Path
import smtplib
import base64
sys.path.append(str(Path(__file__).resolve().parent.parent))
import EmailGenerator as es
from flask import Flask, request, session, flash, redirect, url_for, jsonify
import EmailSend as send

# Create a new Flask application
app = Flask(__name__)
# Set the secret key for the Flask app. This is used for session security.
app.secret_key = "your_secret_key"
email = "defaultemail"

# Configuration for Firebase
config = {
    "apiKey": "AIzaSyAiUacJKkDZ2z-tDMxJMrYifhrKWwoclBo",
    "authDomain": "cc-scanner-db.firebaseapp.com",
    "databaseURL": "https://(default).firebaseio.com",
    "storageBucket": "cc-scanner-db.firebasestorage.app"
}

app.config['GOOGLE_CLIENT_ID'] = '1074903282705-q214r7lsacmorb3kf7q8ansm945s167k.apps.googleusercontent.com'
app.config['GOOGLE_CLIENT_SECRET'] = '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'
app.config['GOOGLE_DISCOVERY_URL'] = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Initialize Firebase
firebase = pyrebase.initialize_app(config)

# Get reference to the auth service and database service
auth = firebase.auth()
db = firebase.database()

# Route for the login page
@app.route("/")
def login():
    return render_template("login.html")

# Route for the signup page
@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/welcome")
def welcome():
    if session.get("is_logged_in", False):
        return render_template("welcome.html", email=session["email"], name=session["name"])
    else:
        return redirect(url_for('login'))

def check_password_strength(password):
    return True

# Route for login result
@app.route("/result", methods=["POST", "GET"])
def result():
    pass


# # Route for user registration
# @app.route("/google_login", methods=["POST", "GET"])
# def google_login():
#     pass

# Set up environment variable to allow HTTP (only for local development)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Set your client secret JSON path
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "../GCal_credentials.json")

@app.route("/google_login", methods=["GET"])
def google_login():
    flow = Flow.from_client_secrets_file(
        client_secrets_file=client_secrets_file,
        scopes=[
            "https://www.googleapis.com/auth/userinfo.email",
            "openid",
            "https://www.googleapis.com/auth/calendar",
            "https://www.googleapis.com/auth/calendar.events",
            "https://www.googleapis.com/auth/gmail.send"  
        ],
        redirect_uri=url_for('google_callback', _external=True)
    )
    
    # 🛠 Correct authorization URL with prompt='consent' to force refresh_token!
    authorization_url, state = flow.authorization_url(
        access_type='offline',          # Needed for refresh token
        include_granted_scopes='true',
        prompt='consent'                 # 🛑 ADD THIS LINE
    )
    
    session["state"] = state
    return redirect(authorization_url)

@app.route("/google_callback")
def google_callback():
    flow = Flow.from_client_secrets_file(
        client_secrets_file=client_secrets_file,
        scopes=[
            "https://www.googleapis.com/auth/userinfo.email",
            "openid",
            "https://www.googleapis.com/auth/calendar",
            "https://www.googleapis.com/auth/calendar.events",
            "https://www.googleapis.com/auth/gmail.send"
        ],
        redirect_uri=url_for('google_callback', _external=True)
    )

    authorization_response = request.base_url + '?' + request.query_string.decode()
    flow.fetch_token(authorization_response=authorization_response)

    if not session["state"] == request.args["state"]:
        return "State mismatch error", 400

    credentials = flow.credentials
    request_session = google.auth.transport.requests.Request()
    id_info = id_token.verify_oauth2_token(
        credentials._id_token,
        request_session,
        audience="1074903282705-q214r7lsacmorb3kf7q8ansm945s167k.apps.googleusercontent.com"
    )

    email = id_info.get("email")
    name = id_info.get("name")
    uid = id_info.get("sub")

    # 🛠 Print credential values to debug if needed
    print("Access Token:", credentials.token)
    print("Refresh Token:", credentials.refresh_token)
    print("Token URI:", credentials.token_uri)
    print("Client ID:", credentials.client_id)
    print("Client Secret:", credentials.client_secret)
    print("Scopes:", credentials.scopes)

    # 🛠 Save to token.json
    token_data = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes
    }

    with open("token.json", "w") as token_file:
        json.dump(token_data, token_file)

    print("token.json created successfully.")

    session["is_logged_in"] = True
    session["email"] = email
    session["name"] = name
    session["uid"] = uid
    session["access_token"] = credentials.token

    fire.initUser(user_id=email, resume="default", role="default")
    gmail = email

    return render_template(
        "homepage.html",
        hasResume=fire.hasResume(gmail),
        intendedRole=fire.getRole(gmail),
        intendedComapny=fire.getCompany(gmail)
    )


@app.route("/logout")
def logout():
    """
    Handle user logout by clearing the session and redirecting to the login page.
    """
    # Clear the user session
    session.clear()

    # Redirect user back to login page
    return redirect(url_for('login'))

# Route for index page
@app.route("/homepage")
def index():
    return render_template("homepage.html", fire.hasResume(session["email"]))

# Route for index page
@app.route("/results")
def results(content):
    return render_template("results.html", content)



@app.route("/process_resume", methods=["POST"])
def process_resume():

    if "resume" not in request.files:
        if (not fire.hasResume(session['email'])): 
            flash("No resume file uploaded", "danger")
            return redirect(url_for('index'))

      # <--- Uploaded file
    if (not fire.hasResume(session['email'])): 
        resume_file = request.files["resume"]
        pdf_reader = PdfReader(resume_file)
    
        # Extract text from all pages
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
        fire.updateResume(session["email"], pdf_text)
    
    result = es.generateEmail(role=request.form.get('role'), collegeName=request.form.get('college'), companyNames=[request.form.get('company')], resumeData=fire.getResume(session['email']))
    session["resumeData"] = fire.getResume(session['email'])
    session["personDataJSON"] = result[5]
    session['personSummary'] = result[1]
    session['pfp'] = result[0]
    session['targetMail'] = result[2]
    session['subjectLine'] = result[4]
    return render_template("results.html", contents = result[3], personSummary = result[1], subjectLine=result[4], pfp=result[0])


def generate_oauth2_string(username: str, access_token: str) -> str:
    """
    Build the base64-encoded XOAUTH2 auth string.
    """
    auth_str = f"user={username}\x01auth=Bearer {access_token}\x01\x01"
    return base64.b64encode(auth_str.encode()).decode()

@app.route("/update_email", methods=["POST"])
def update_email():
    print("hello" + str(request.form.get('action')))
    if (request.form.get('action') == "update"):
        session['subjectLine'] = request.form.get('subjectline')
        result = es.editEmail(request.form.get('email'), request.form.get('edits'), "https://i.seadn.io/gae/y2QcxTcchVVdUGZITQpr6z96TXYOV0p3ueLL_1kIPl7s-hHn3-nh8hamBDj0GAUNAndJ9_Yuo2OzYG5Nic_hNicPq37npZ93T5Nk-A?auto=format&dpr=1&w=1000", session['personSummary'], session['email'], session['resumeData'], session['personDataJSON'], session['subjectLine'])
        return render_template("results.html", contents = result[3], personSummary = result[1], subjectLine = request.form.get('subjectline'), pfp=result[0])
    else:
        send.gmail_send_message('rab547@cornell.edu', session['email'], session['subjectLine'], request.form.get('email'))
        return render_template("login.html")


@app.route("/send_email", methods=["POST"])
def send_email():
    print("sending email")
    session['subjectLine'] = request.form.get('subjectline')
    send.gmail_send_message('rab547@cornell.edu', "mg2476@cornell.edu", session['subjectLine'], request.form.get('email'))

    if (session['targetMail'] == None):
        print("the other thing")
        flash("No email found for this user")
    else:
        print("trying to send")
    return render_template("login.html")
    

if __name__ == "__main__":
    app.run(debug=True)
