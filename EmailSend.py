import base64
from email.message import EmailMessage

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

import os


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def create_service(credentials_path=None, token_path=None):
    print("VVVV")
    if credentials_path is None or token_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        if token_path is None:
            token_path = os.path.join(project_root, "token.json")
          
        if credentials_path is None:
            credentials_path = os.path.join(project_root, "dataton/GCal_credentials.json")

    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("CREEEE" + credentials_path)
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES
            )
            creds = flow.run_local_server(port=0)
            
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    
    # Return calendar service
    return build("gmail", "v1", credentials=creds)

def gmail_send_message(recipientEmail, senderEmail, subjectLine, content):

  try:
    service = create_service()
    message = EmailMessage()

    message.set_content(content)

    message["To"] = recipientEmail
    message["From"] = senderEmail
    message["Subject"] = subjectLine

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    # pylint: disable=E1101
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    print(f'Message Id: {send_message["id"]}')
  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None
  return send_message


if __name__ == "__main__":
    x = gmail_send_message("rab547@cornell.edu", "mg2476@cornell.edu", "TESTING", "TESTING")
    print("sent")
    print(x)