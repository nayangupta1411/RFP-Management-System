import google.generativeai as genai
import os,re
from dotenv import load_dotenv
from flask import json, jsonify
import uuid
from ..formatting.request_content_cleaning import CleanJsonOutput
from ...utils.generate_uid import GenerateUID



class AiModelRequest:
    def __init__(self,req_data):
        self.req_data=req_data
        self.requester_name=self.req_data["name"]
        self.request_email=self.req_data["email"]
        self.request_org=self.req_data["org"]
        self.request_contact=self.req_data["contact"]
        self.request_vendor=self.req_data["vendor"]
        self.request_message=self.req_data["message"] 
        self.__api_key=None
        self.__unique_id=None
        self.vendor_list=[]
        
    def set_unique_uid(self):
        uid=GenerateUID()
        self.__unique_id=uid.unique_uid()

    
    def get_unique_uid(self):
        if self.__unique_id is None:
            self.set_unique_uid()
        return self.__unique_id
    
    def set_api_key(self):
        self.__api_key=os.getenv("GENAI_KEY")

    def get_api_key(self):
        if self.__api_key is None:
            self.set_api_key()
        return self.__api_key
    
    
    def prompt(self):
        
        prompt = f"""
    You MUST output ONLY a valid JSON object.
    No markdown, no ```json, no explanation.
    
    Output ONLY this structure:

    {{
        "Subject": "#{self.get_unique_uid()}: <subject line>",
        "Body": "<plain text email with real line breaks>"
    }}

    BODY RULES:
    - Use REAL line breaks (\\n only for JSON escaping).
    - Email must look clean when converted to Python string.
    - No markdown (#, **, ---).
    - Use simple text formatting.
    - Add this signature automatically at the end:

      Best Regards,
      {self.requester_name}
      {self.request_org}
      Contact: {self.request_contact}

    SECTIONS REQUIRED IN BODY:
    1. Introduction
    2. Requirement Summary
    3. Detailed Breakdown
    4. Commercial Details
    5. Additional Notes
    6. Signature (auto-filled)

    Now generate the JSON for this requirement:

    \"\"\"{self.request_message}\"\"\"
    """
        return prompt
    
    
    def mail_content(self):
        genai.configure(api_key=self.get_api_key())
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(self.prompt())
        raw=response.text.strip()
        print(f'78 : raw data : {raw}')
        fine_content=CleanJsonOutput(raw) 
        cleaned_json_content = fine_content.clean_json_output()
        print(f'81: cleaned_json_content : {cleaned_json_content}')
        ai_request_content=json.loads(cleaned_json_content) 
        print(f'83: subject : {ai_request_content["Subject"]}')
        try:
            return ai_request_content
        except json.JSONDecodeError as e:
            print("JSON parsing failed. Raw model output:", raw)
            raise e
    
    def list_of_vendors(self):
        ven=self.request_vendor
        for i in range(len(ven)):
            self.vendor_list.append(ven[i].get('label')) 
        return list(set(self.vendor_list))
    
    def mail_creation(self):
        content=self.mail_content()
        vendors=self.list_of_vendors()
        return {"uid":self.__unique_id,
                "sender":self.request_email,
                "subject":content["Subject"],
                "body": content["Body"],
                "vendors": vendors}

        
