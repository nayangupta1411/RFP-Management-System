from flask import g

class UniqueUidList:
    def __init__(self,db):
        self.db=db
        self.fetchUIDs=None
    
    def fetch_uids(self):
        self.fetchUIDs = list(self.db.user_request.find({}, {"_id": 0, "uid": 1}).sort("created_at", -1))
        return self.fetchUIDs