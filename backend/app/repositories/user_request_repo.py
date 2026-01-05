from ..dashboard.models.ai_model_request import AiModelRequest
from ..utils.datetime_util import DateTime
from flask import g

class UserRequestRepo:
    def __init__(self, req: AiModelRequest):
        self.name=req.requester_name 
        self.email=req.request_email
        self.org=req.request_org
        self.contact=req.request_contact
        self.vendor=req.list_of_vendors()
        self.message=req.request_message
        self.uid=req.get_unique_uid()
        self.time=DateTime.time_utc()
    
    def create_request(self):
        result = g.db.user_request.insert_one({
            "uid": self.uid,
            "name":self.name,
            "email":self.email,
            "organization":self.org,
            "contact no." : self.contact,
            "vendors" : self.vendor,
            "message": self.message,
            "created_at":self.time      
        })
        return str(result.inserted_id)
    
 
        