import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
To='mostaf7583@gmail.com'
def send_email_with_attachment(To):
    # Set up the SMTP server for Outlook
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    smtp_username = 'mostafa7589@outlook.com'
    smtp_password = 'sallam2000'

    # Set up the email message
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = To
    msg['Subject'] = 'Subject line of the email'

    body = 'Hello, This is a test email!'
    msg.attach(MIMEText(body, 'plain'))

    # Open the file in binary mode
    filename='file.txt'
    attachment = open(filename, "rb")

    # Instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_username, To, text)
        print('Email sent successfully!')



# fetch the emails from the csv file
import pandas as pd
df = pd.read_csv('data.csv')
emails = df['Email'].values
for email in emails:
    send_email_with_attachment(email)
