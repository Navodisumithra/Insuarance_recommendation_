import os
import ssl
import smtplib
from email.message import EmailMessage

# Fix import
from dotenv import load_dotenv  

# load variables from .env
load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # SSL port

# These must be ENV VARS (not raw values here)
SENDER_EMAIL = os.getenv("SENDER_EMAIL")          
APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")    

def send_email(to_email: str, subject: str, body: str):
    if not SENDER_EMAIL or not APP_PASSWORD:
        raise RuntimeError("SENDER_EMAIL and EMAIL_APP_PASSWORD must be set as environment variables.")

    msg = EmailMessage()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    send_email("navodipahalawela@gmail.com", "Test email from Python", "Hello — this is a test.")
    print("Email sent.")
