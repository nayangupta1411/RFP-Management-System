import smtplib
import ssl
from email.message import EmailMessage
import os
from flask import jsonify

class RequestMail:
    def __init__(self,subject,body,vendor):
        self.vendor=vendor
        self.subject=subject
        self.body=body
        self.__EMAIL=os.getenv("SENDER_EMAIL")
        self.__APP_PASSWORD=os.getenv("APP_PASSWORD")
        self.__SMTP_SERVER=os.getenv("SMTP_SERVER")
        self.__SMTP_PORT=int(os.getenv("SMTP_PORT"))
    
        
    def send_email(self):
        print(self.__SMTP_SERVER,self.__SMTP_PORT)
        try:
            server=smtplib.SMTP(self.__SMTP_SERVER, self.__SMTP_PORT)
                
            server.ehlo()
            server.starttls(context=ssl.create_default_context())
            server.ehlo()
            
            print("🔐 Logging in...")
            server.login(self.__EMAIL, self.__APP_PASSWORD)
            
            for vendor in self.vendor:
                message = EmailMessage()
                message["From"] = self.__EMAIL
                message["To"] = vendor
                message["Subject"] = self.subject
                message.set_content(self.body)
                
                print("📤 Sending email...")
                server.send_message( message)
                
            server.quit()
                
            print("✅ Email sent successfully!")
            return jsonify({"status": "sent", "to": self.vendor})
        except Exception as e:
            print("❌ Error sending email:", str(e))
            return {"status": "error", "message": str(e)}
            