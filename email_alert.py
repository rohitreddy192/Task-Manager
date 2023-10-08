import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(to_email, subject, message):
    from_email = 'email@gmail.com' #Email ID from which the message should be sent
    smtp_server = 'smtp.gmail.com' 
    smtp_port = 587 
    smtp_username = 'email@gmail.com'
    smtp_password = 'tfbcahdusaehhdehdjshdkl' 

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())






























#--> Default email using smtp

