from database.connection import mongo

def ai_create_indexes():
    db = mongo.db  # This refers to the RFP database

    # Create collection: ai_user_request (Mongo creates it automatically)
    ai_user_request = db.ai_user_request  

    # Create Indexes (Auto schema-like rules)
    ai_user_request.create_index([("uid", 1)], name="ai_idx_user_request_uid")

    print("✔ MongoDB database & ai_user_request collection initialized successfully.")