"""SMTP Mail Send"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from langchain_core.messages import AIMessage, HumanMessage


def send_email(sender, receiver, subject, message):
    """Sending email"""
    server = smtplib.SMTP("localhost", port=25)

    msg_body = "Conversation History:<br/>"
    for each_message in message:
        if isinstance(each_message, AIMessage):
            msg_body = "".join([msg_body, "AI: ", each_message.content, "<br/>"])
        elif isinstance(each_message, HumanMessage):
            msg_body = "".join([msg_body, "Human: ", each_message.content, "<br/>"])
        else:
            print("Message Type:" + type(each_message))

    # mail_message = MIMEText(msg_body, "plain")
    mail_message = MIMEMultipart("alternative")
    mail_message["Subject"] = subject
    mail_message["From"] = sender
    mail_message["To"] = receiver

    content_body = MIMEText(msg_body, "html")
    mail_message.attach(content_body)

    server.sendmail(sender, receiver, mail_message.as_string())

    server.quit()
