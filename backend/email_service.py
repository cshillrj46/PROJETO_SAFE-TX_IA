# File: backend/email_service.py

import smtplib
from email.message import EmailMessage

GMAIL_USER = "cristianohill35@gmail.com"  # 🔁 Substitua pelo seu
GMAIL_PASS = "ivbn aebm hgbn iehj"    # 🔁 Substitua pela senha de app gerada

def send_email_alert(recipient_email: str, subject: str, content: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = recipient_email
    msg.set_content(content)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASS)
            smtp.send_message(msg)
            print("[E-mail] ✅ Sent successfully.")
    except Exception as e:
        print(f"[E-mail] ❌ Failed to send: {e}")
