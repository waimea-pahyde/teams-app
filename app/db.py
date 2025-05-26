#===========================================================
# Database Related Functions
#===========================================================

from libsql_client import create_client_sync
from dotenv import load_dotenv
import os


# Load the Turso API keys from the .env file
load_dotenv()
TURSO_URL = os.getenv("TURSO_URL")
TURSO_KEY = os.getenv("TURSO_KEY")

# Define the locations of our DB files
DB_FOLDER   = os.path.join(os.path.dirname(__file__), "db")
SCHEMA_FILE = os.path.join(DB_FOLDER, "schema.sql")

client = None

#-----------------------------------------------------------
# Connect to the Turso DB and return the connection
#-----------------------------------------------------------
def connect_db():
    global client
    if client == None:
        client = create_client_sync(url=TURSO_URL, auth_token=TURSO_KEY)
    return client


#-----------------------------------------------------------
# Initialise the DB from the schema file
#-----------------------------------------------------------
def init_db():
    client = connect_db()
    with open(SCHEMA_FILE, "r") as f:
        client.execute(f.read())

