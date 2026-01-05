from flask_pymongo import PyMongo
from database.config import MONGO_URI


mongo = PyMongo()

def init_db(app):
    app.config["MONGO_URI"] = MONGO_URI
    mongo.init_app(app)
    
    from .schemas.request.request_database  import create_indexes
    create_indexes()
    
    from .schemas.request.ai_request_database  import ai_create_indexes
    ai_create_indexes()
    
    from .schemas.response.ai_response_database import ai_create_indexes
    ai_create_indexes()

def get_db():
    if mongo.db is None:
        raise RuntimeError("MongoDB not initialized. Call init_db(app) first.")
    return mongo.db