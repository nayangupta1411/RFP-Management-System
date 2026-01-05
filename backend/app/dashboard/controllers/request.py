from flask import request,jsonify
from ..models.ai_model_request import AiModelRequest
from ...repositories.user_request_repo import UserRequestRepo
from ...repositories.ai_user_request_repo import AiUserRequestRepo
from ..mail_service.request_mail import RequestMail


def make_request():
    try: 
        if request.method=='POST':
            if not request.is_json:
                return jsonify({"error": "Request must be JSON"}), 400
            get_request=request.get_json()
            print("get_request: ",get_request)
            model=AiModelRequest(get_request)
            mail_content=model.mail_creation()
            print(f'mail content: {model.mail_content()}')
            print(model.mail_creation())
            print(f'subject : {mail_content["subject"]}, body: {mail_content["body"]}, vendors: {mail_content["vendors"]}')
            req_repo=UserRequestRepo(model)
            req_repo.create_request()
            ai_req_repo=AiUserRequestRepo(mail_content)
            ai_req_repo.user_request_ai_mail()
            sent_mail=RequestMail(mail_content["subject"],mail_content["body"],mail_content["vendors"])
            sent_mail.send_email()
            return jsonify({"get_request_data":get_request}),200
    except Exception as e:
        return jsonify({"error": str(e)})
