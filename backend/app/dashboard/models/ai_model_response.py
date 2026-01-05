from flask import json
import google.generativeai as genai
import os
from ..formatting.response_content_cleaning import CleanResponseOutput
from ...repositories.ai_vendor_response_repo import AiVendorResponseRepo
from ...repositories.fetch_ai_vendor_response_checker_repo import FetchAiVendorResponseCheckerRepo


class VendorAnalyzer:

    def __init__(self,db):
        self.db=db
        genai.configure(api_key=os.getenv("GENAI_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        
    def get_single_vendor_prompt(self,vendor_email_id,vendor_response):
        prompt = f"""
                You are an AI procurement analyst.

                Analyze the following vendor response and produce a structured analysis.

                Vendor Name: {vendor_email_id}

                Vendor Response:
                {vendor_response}

                Return the result STRICTLY in JSON with the following keys:

                summary: short summary of proposal
                pricing: pricing details or "Not mentioned"
                delivery: delivery timeline or "Not mentioned"
                terms: warranty / terms & conditions
                completeness: Complete / Partial / Incomplete
                rating: number between 0 and 5
                recommendation_status: one of
                    - RECOMMENDED
                    - NOT_RECOMMENDED
                    - NEEDS_REVIEW
                    - COMPARE_WITH_OTHERS
                recommendation_reason: 1 or 2 line justification

                Rules:
                    - Be concise and professional
                    - Do not reference other vendors
                    - Do not invent missing data
                    - Choose recommendation_status logically
                    - Output ONLY valid JSON
                    - No markdown, no ```json, no explanation.
                """
        return prompt


    def analyze_vendor_responses(self, vendor_replies):
        clean_response=CleanResponseOutput()
        result = []
        for v in vendor_replies:
            uid=clean_response.safe_decode(v.get('uid', ''))
            vendor_email_id=clean_response.safe_decode(v.get('from', 'Unknown'))
            vendor_response=clean_response.safe_decode(v.get('body', ''))
            vendor_reply_at=clean_response.safe_decode(v.get('reply_at', ''))
            
            check_db_status=FetchAiVendorResponseCheckerRepo(self.db,uid,vendor_email_id,vendor_reply_at)
            if check_db_status.is_already_analyzed():
                continue
        
            prompt = self.get_single_vendor_prompt(vendor_email_id, vendor_response)
            response = self.model.generate_content(prompt)
            
            try:
                ai_output = json.loads(response.text.strip())
            except Exception:
            # fallback (should be rare if prompt is strict)
                ai_output = {
                "summary": response.text,
                "pricing": None,
                "delivery": None,
                "terms": None,
                "completeness": "Unknown",
                "rating": None,
                "recommendation_status": "NEEDS_REVIEW",
                "recommendation_reason": "AI output could not be parsed"
            }
            
            ai_response_repo=AiVendorResponseRepo(self.db,ai_output,uid,vendor_email_id,vendor_reply_at)
            ai_response_repo.create_vendor_ai_response()
            result.append({
            "uid":uid,
            "vendor": vendor_email_id,
            "analysis": response.text.strip()
             })

        try:
            return result
        
        except Exception as e:
            print("Gemini Error:", e)
            return None
