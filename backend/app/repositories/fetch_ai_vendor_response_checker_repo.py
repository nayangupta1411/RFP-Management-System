class FetchAiVendorResponseCheckerRepo:
    
    def __init__(self,db,uid,vendor_email_id,vendor_reply_at):
        self.uid = uid
        self.vendor_email_id = vendor_email_id
        self.vendor_reply_at = vendor_reply_at
        self.db=db
    
    def is_already_analyzed(self):
        doc = self.db.ai_vendor_response.find_one(
            {
                "uid": self.uid,
                "vendor": self.vendor_email_id,
                "reply_at": self.vendor_reply_at,
                "status": "ANALYZED"
            },
            {"_id": 1}
        )
        return doc is not None