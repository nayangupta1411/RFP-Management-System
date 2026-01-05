from flask import Blueprint,request as flask_request
from ..dashboard.controllers.request import make_request
from ..dashboard.controllers.response import Response
from ..repositories.fetch_ai_user_request_repo import FetchAiUserRequestRepo

dashboard_route=Blueprint('dashboard',__name__)

@dashboard_route.route('/request',methods=['POST','GET'])
def request():
    return make_request()

@dashboard_route.route('/response',methods=['POST','GET'])
def response():
    data=flask_request.get_json()
    uid=data.get("uid")
    vendors=data.get("vendors")
    response=Response(uid=uid,vendors=vendors)
    return response.get_response()

@dashboard_route.route('/getRequests',methods=['POST','GET'])
def getResponses():
    fetch_ai_repo=FetchAiUserRequestRepo()
    return fetch_ai_repo.fetch_ai_user_request()