import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def sendGmailToProfesser(to_Recipent, subject, content):
    try:
        # Gmail account details
        gmail_user = 'phuminsathipchan@gmail.com'
        gmail_password = 'jellrmwsbwdrcree'

        # Recipient email address
        to = to_Recipent

        # Create a message
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = to
        msg['Subject'] = subject

        # Message body
        body = content
        msg.attach(MIMEText(body, 'plain'))

        # Send the message using Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        text = msg.as_string()
        server.sendmail(gmail_user, to, text)
        server.quit()
        return True
    except:
        return False
