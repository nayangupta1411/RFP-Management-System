from flask import g

class FetchAiVendorResponseRepo:
    
    def __init__(self,**kwargs):
        self.uid = kwargs.get("uid")
        self.vendor_email_id = kwargs.get("vendor_email_id")
        self.vendor_reply_at = kwargs.get("vendor_reply_at")
        self.response={}

    
    def fetchResponse(self):
        self.response=g.db.ai_vendor_response.find_one(
            {"uid": self.uid,
             "vendor": {
                   "$regex": self.vendor_email_id,
                    "$options": "i"
                }
             })  
        print(f'response : {self.response}, type of response : {type(self.response)}') 
        return {"response":self.response, "vendor_email":self.vendor_email_id}
    
    
    