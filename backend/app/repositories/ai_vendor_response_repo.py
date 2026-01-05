from ..utils.datetime_util import DateTime

class AiVendorResponseRepo:
    
    def __init__(self,db,aiResponse,uid,vendor_email,vendor_reply_at):
        self.db=db
        self.uid=uid
        self.vendor=vendor_email
        self.aiResponse=aiResponse
        self.summary=self.aiResponse.get("summary")
        self.pricing=self.aiResponse.get("pricing")
        self.delivery=self.aiResponse.get("delivery")
        self.terms=self.aiResponse.get("terms")
        self.completeness=self.aiResponse.get("completeness")
        self.rating=self.aiResponse.get("rating")
        self.recommendation_status=self.aiResponse.get("recommendation_status")
        self.recommendation_reason=self.aiResponse.get("recommendation_reason")
        self.vendor_reply_at=vendor_reply_at
        self.time=DateTime.time_utc()
        self.document=None
    
    def collection_structure(self):
        self.document = {
            "uid": self.uid,
            "vendor": self.vendor,
            "reply_at": self.vendor_reply_at,

            "analysis": {
                "summary": self.summary,
                "pricing": self.pricing,
                "delivery": self.pricing,
                "terms": self.terms,
                "completeness": self.completeness
            },

            "rating": self.rating,
            "recommendation_status": self.recommendation_status,
            "recommendation_reason": self.recommendation_reason,

            "status": "ANALYZED",
            "processed_at": self.time
        }
        return self.document
    
    def create_vendor_ai_response(self):
        result = self.db.ai_vendor_response.update_one({
            "uid": self.uid,
            "vendor":self.vendor
            },{
                "$set": self.collection_structure()
            },
            upsert=True)
        
        return str(result.upserted_id)
        
    