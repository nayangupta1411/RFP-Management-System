from flask import request,jsonify
from ...repositories.fetch_ai_vendor_response_repo import FetchAiVendorResponseRepo

class Response:
    
    def __init__(self,**kwargs):
        self.uid=kwargs.get("uid")
        self.vendors=kwargs.get("vendors")
        
    def get_response(self):
        
        if isinstance(self.vendors,list):
            result=[]
            for vendor in self.vendors:
                flag=False
                fetch_responses=FetchAiVendorResponseRepo(uid=self.uid,vendor_email_id=vendor)
                fetched_data=fetch_responses.fetchResponse()  
                response_data=fetched_data["response"]
                if response_data:
                    flag=True
                    result.append({"vendor_email":vendor,
                                    "rating": response_data.get("rating"), 
                                    "recommendation_status": response_data.get("recommendation_status"),
                                    "recommendation_reason":response_data.get("recommendation_reason"),
                                    "analysis": response_data.get("analysis"),
                                    "flag": flag})
                else:
                    result.append({"vendor_email":vendor,
                                "rating": None, 
                                "recommendation_status": None,
                                "recommendation_reason": None,
                                "analysis": "No Review",
                                "flag": flag})
          
            print(f'response result : {result}')
       
            return result
        

