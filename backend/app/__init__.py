from flask import Flask, g, request
from flask_cors import CORS
from .api.routes import dashboard_route
from database.connection import init_db,get_db

def create_app():
    app=Flask(__name__)
    CORS(app)
    init_db(app)
    
    @app.before_request
    def before_request():
        g.db = get_db()
        g.request_id = request.headers.get("X-Request-ID")
    
    @app.after_request
    def after_request(response):
        response.headers["X-App"] = "RFP-System"
        return response
    
    @app.teardown_appcontext
    def teardown_appcontext(exception=None):
        if exception:
            app.logger.error(exception)
            
    app.register_blueprint(dashboard_route,url_prefix='/dashboard')
    return app
