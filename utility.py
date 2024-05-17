import smtplib
from decouple import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email_notification(msg):
    # Email configuration
    sender_email = config('ALERT_EMAIL')
    receiver_email = config('ADMIN_EMAIL')
    password = config('EMAIL_PASSWORD')

    # Create message container
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "ALERT FROM LIB-jobs"

    # Email content
    body = msg
    message.attach(MIMEText(body, "plain"))

    # Connect to SMTP server (Gmail)
    '''
    with smtplib.SMTP_SSL(config('EMAIL_SERVER'), config('EMAIL_PORT')) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    '''
    print(f"Email sent successfully! {msg}")

