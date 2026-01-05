from dotenv import load_dotenv
import sys,os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Insert project root at highest priority
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Load environment variables
load_dotenv()
  
from app import create_app
  
app=create_app()
app.config["JSON_AS_ASCII"] = False

if __name__=='__main__':   
    app.run(debug=True)
