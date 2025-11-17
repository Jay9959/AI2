# def send_reset_email(email: str, reset_link: str):
#     print("\n📧 Sending password reset email to:", email)
#     print("🔗 Reset link:", reset_link)
#     # Later you can add real SMTP (Gmail/SendGrid)


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

def send_reset_email(to_email: str, reset_link: str):
    try:
        subject = "Password Reset Request"
        body = f"""
        Hi there,
        
        We received a request to reset your password.
        Click the link below to reset it:
        
        {reset_link}
        
        This link will expire in 15 minutes.
        
        If you didn’t request this, please ignore this email.
        
        Thanks,
        Your App Team
        """

        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())

        print(f"✅ Reset link sent to {to_email}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")
