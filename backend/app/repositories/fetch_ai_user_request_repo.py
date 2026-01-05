from flask import g

class FetchAiUserRequestRepo:
    
    def __init__(self):
        self.ai_requests=None
    
    def fetch_ai_user_request(self):
        pipeline = [{
        "$lookup": {
            "from": "user_request",        # collection to join
            "localField": "uid",            # ai_user_request.uid
            "foreignField": "uid",          # user_request.uid
            "as": "user_request_data"
        }
        },
        {
            "$unwind": "$user_request_data"    # flatten array
        },
        {
            "$addFields": {
                "created_at": "$user_request_data.created_at"
        }
        },
        {
            "$project": {
                "user_request_data": 0          # remove joined object if not needed
        }
        }
        ]

        self.ai_requests = list(g.db.ai_user_request.aggregate(pipeline))
        print(f'ai_requests :{self.ai_requests}')
        return self.ai_requests
        