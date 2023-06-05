from email.message import EmailMessage
from dotenv import load_dotenv
import ssl, smtplib, os

load_dotenv(r'git\.env')
email_password = os.getenv('EMAIL_PASSWORD')

def send_email(receiver: str, attachment_path = None, password = email_password):
    """
    Sends an email with the values provided.
    """

    sender = 'randommailaccc@gmail.com'
    subject = 'Qr Code'
    body = """
    To Person <{}>

    See the attachment for the qr code. 
    """.format(receiver)

    em = EmailMessage()

    em['From'] = sender
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(body)

    # Add the attachment if provided
    if attachment_path is not None:
        with open(attachment_path, 'rb') as f:
            attachment_data = f.read()
            em.add_attachment(attachment_data, maintype='application', subtype='octet-stream', filename=attachment_path.split('/')[-1])

    # Send the email
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        if password is not None:
            smtp.login(sender, password)
        smtp.sendmail(sender, receiver, em.as_string())

    print('Email sent successfully.')