from ..dashboard.mail_service.response_mail import ResponseMail
from ..dashboard.models.ai_model_response import VendorAnalyzer

def process_vendor_responses_job(db):
    print("CRON JOB STARTED: Processing vendor responses")
    
    response_mail=ResponseMail(db)
    responses=response_mail.fetch_unread_replies()
    print(f'responses : {responses}')
    
    if not responses:
        print("No new vendor replies found")
        return
    
    analyzer=VendorAnalyzer(db)
    analyze_content=analyzer.analyze_vendor_responses(responses)
    print(f'analyze_content : {analyze_content}')
