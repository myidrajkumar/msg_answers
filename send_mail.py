"""SMTP Mail Send"""

import smtplib
from email.mime.text import MIMEText


def send_email(sender, receiver, subject, message):
    """Sending email"""
    server = smtplib.SMTP("localhost", port=25)

    mail_message = MIMEText(message, "plain")
    mail_message["Subject"] = subject
    mail_message["From"] = sender
    mail_message["To"] = receiver

    server.sendmail(sender, receiver, mail_message.as_string())

    server.quit()
