from database.connection import mongo

def create_indexes():
    db = mongo.db  # This refers to the RFP database

    # Create collection: user_request (Mongo creates it automatically)
    user_request = db.user_request  

    # Create Indexes (Auto schema-like rules)
    user_request.create_index([("email", 1)], name="idx_user_request_email")
    user_request.create_index([("uid", 1)], unique=True, name="idx_user_request_uid")

    print("✔ MongoDB database &  user_request collection initialized successfully.")
 
