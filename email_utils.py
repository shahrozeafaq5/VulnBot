import smtplib
from email.message import EmailMessage
from config import GMAIL_USER, GMAIL_APP_PASSWORD, TO_EMAIL


def send_email(subject, body, html=False):
    msg = EmailMessage()
    msg["From"] = GMAIL_USER
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject

    if html:
        msg.set_content("Your email client does not support HTML.")
        msg.add_alternative(body, subtype="html")
    else:
        msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        smtp.send_message(msg)