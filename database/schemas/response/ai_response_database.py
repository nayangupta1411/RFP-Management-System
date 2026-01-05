from database.connection import mongo

def ai_create_indexes():
    db = mongo.db  # This refers to the RFP database

    # Create collection: ai_vendor_response (Mongo creates it automatically)
    ai_vendor_response = db.ai_vendor_response  

    # Create Indexes (Auto schema-like rules)
    ai_vendor_response.create_index([("uid", 1)], name="ai_idx_vendor_response_uid")

    print("✔ MongoDB database & ai_vendor_response collection initialized successfully.")