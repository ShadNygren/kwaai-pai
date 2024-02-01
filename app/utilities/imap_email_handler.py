from imaplib import IMAP4_SSL
from email import message_from_bytes
from email.utils import parsedate_to_datetime

class ImapEmailHandler:
    def __init__(self, user, password, imap_server='imap.gmail.com') -> None:
        self.user = user
        self.password = password
        self.imap_server = imap_server
        self.mail = IMAP4_SSL(imap_server)
        self.mail.login(user, password)
        self.mail.select('Inbox')

    def search_emails(self, key, value = None ):
        _, data = self.mail.search(None, key, value)
        mail_id_list = data[0].split()
        return mail_id_list

    def fetch_emails(self, mail_id_list):
        msgs = []
        for num in mail_id_list:
            typ, data = self.mail.fetch(num, '(RFC822)')
            msgs.append(data)
        return msgs
    
    def process_emails(self, emails_data: list) -> list:
        processed_emails = []

        for email_data in emails_data:
            raw_email = email_data[0][1]
            msg = message_from_bytes(raw_email)

            subject = msg.get('Subject', '')
            sender = msg.get('From', '')
            date_str = msg.get('Date', '')

            date = parsedate_to_datetime(date_str) if date_str else None

            body = self.extract_body(msg)

            processed_email = {
                'Subject': subject,
                'From': sender,
                'Date': date,
                'Body': body,
            }

            processed_emails.append(processed_email)

        return processed_emails

    def extract_body(self, msg):
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                return part.get_payload()

        return ''