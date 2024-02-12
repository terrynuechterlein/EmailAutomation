import imaplib
import email
import configparser
from email.header import decode_header

# Configuration
config = configparser.ConfigParser()
config.read('config.ini')
imap_url = config['DEFAULT']['ImapUrl']
email_user = config['DEFAULT']['EmailUser']
email_password = config['DEFAULT']['EmailPassword']

# Connect to the email server
mail = imaplib.IMAP4_SSL(imap_url)
mail.login(email_user, email_password)

mail.select('inbox')

def move_email(mail_uid, label_name):
    result, copy_response = mail.uid('COPY', mail_uid, label_name)
    if result == 'OK':
        mail.uid('STORE', mail_uid, '+FLAGS', r'(\Deleted)')
        mail.expunge()
    else:
        print(f"Could not move email UID {mail_uid} to {label_name}: {copy_response}")

# Function to search and process emails
def process_emails():
    mail.select('inbox')
    type, data = mail.uid('search', None, 'ALL')  # Use UID search
    mail_uids = data[0].split()

    for mail_uid in mail_uids:
        typ, data = mail.uid('fetch', mail_uid, '(RFC822)')
        email_message = email.message_from_bytes(data[0][1])

        from_email = email.utils.parseaddr(email_message['From'])[1]
        subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))

        # Adjusted rules for moving emails
        if from_email == "jobs-noreply@linkedin.com":
            if "your application was viewed" in subject or "your application was sent to" in subject:
                move_email(mail_uid, 'LinkedInSpam')

        # Corrected indentation
        if from_email == "alerts@ziprecruiter.com":
            move_email(mail_uid, '"Job Alerts"')
        if from_email == "jobalerts-noreply@linkedin.com":
            move_email(mail_uid, '"Job Alerts"')
        if from_email == "indeedapply@indeed.com":
            move_email(mail_uid, '"Job Alerts"')
        if from_email == "info@wayup.com":
            move_email(mail_uid, '"Job Alerts"')
        if from_email == "noreply@redditmail.com":
            move_email(mail_uid, '"Social Media"')

# Call the function to process emails
process_emails()

# Close the connection
mail.logout()
