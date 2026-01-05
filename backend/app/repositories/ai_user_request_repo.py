from flask import g

class AiUserRequestRepo:
    
    def __init__(self,mail):
        self.uid=mail["uid"]
        self.subject=mail["subject"]
        self.body=mail["body"]
        self.receivers=mail["vendors"]
        self.sender=mail["sender"]
    
    def user_request_ai_mail(self):
        result = g.db.ai_user_request.insert_one({
            "uid": self.uid,
            "sender":self.sender,
            "receivers" : self.receivers,
            "subject": self.subject,
            "body":self.body      
        })
        return str(result.inserted_id)
        
        
    
    
    
    
 
    