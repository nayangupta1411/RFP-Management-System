from datetime import timezone,datetime
import time
import imaplib
import email
import os
from contextlib import contextmanager
from ...services.access_uids import AccessUID
from ..formatting.response_content_cleaning import CleanResponseOutput

class ResponseMail:
    def __init__(self,db):
        self.__EMAIL=os.getenv("SENDER_EMAIL")
        self.__APP_PASSWORD=os.getenv("APP_PASSWORD")
        self.__IMAP_SERVER=os.getenv("IMAP_SERVER")
        self.__IMAP_PORT=os.getenv("IMAP_PORT")
        self.db=db
    
    @contextmanager
    def imap_connection(self):
        mail = imaplib.IMAP4_SSL(self.__IMAP_SERVER, self.__IMAP_PORT)  
        try:
            mail.login(self.__EMAIL, self.__APP_PASSWORD)
            print("login successful!")
            mail.select("inbox")
            yield mail
        finally:
            try:
                mail.close()
            except Exception:
                pass
            mail.logout()
    
    def search_by_subject(self,mail, uid):
        search_query = f'(SUBJECT "{uid}")'
        status, messages = mail.search(None, search_query)
        if status != "OK":
            return []
        return messages[0].split()
    
    def parse_email_message(self, msg, cleaner):
        sender = cleaner.safe_decode(msg.get("From"))
        subject = cleaner.safe_decode(msg.get("Subject"))

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain" and not part.get_filename():
                    payload = part.get_payload(decode=True)
                    body += cleaner.safe_decode(payload)
        else:
            payload = msg.get_payload(decode=True)
            body = cleaner.safe_decode(payload)

        return sender, subject, body.strip()


    def fetch_unread_replies(self):
        print("fetch_unread_replies initiated !")
        clean_response=CleanResponseOutput()
        accessUid=AccessUID(self.db)
        valid_uids = accessUid.get_uid_list()
        replies = []
        with self.imap_connection() as mail:
            for uid in valid_uids:
                email_ids=self.search_by_subject(mail,uid)     
                for eid in email_ids:
                    status, data = mail.fetch(eid, "(BODY.PEEK[] INTERNALDATE)")
                    print(f'status message : {status}')
                    msg = email.message_from_bytes(data[0][1])
                    internal_date = imaplib.Internaldate2tuple(data[0][0])
                    reply_at = datetime.fromtimestamp(
                        time.mktime(internal_date),
                        tz=timezone.utc
                    )
                    sender, subject, body = self.parse_email_message(msg, clean_response)
                    
                    replies.append({
                    "uid": uid,
                    "from": sender,
                    "subject": subject,
                    "body": body.strip(),
                    "reply_at":reply_at
                })

        return replies
