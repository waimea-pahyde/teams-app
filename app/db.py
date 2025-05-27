#===========================================================
# Database Related Functions
#===========================================================

from libsql_client import create_client_sync
from dotenv import load_dotenv
import os


# Load Turso environment variables from the .env file
load_dotenv()
TURSO_URL = os.getenv("TURSO_URL")
TURSO_KEY = os.getenv("TURSO_KEY")

# Define the locations of our DB files
DB_FOLDER   = os.path.join(os.path.dirname(__file__), "db")
SCHEMA_FILE = os.path.join(DB_FOLDER, "schema.sql")

# Track the DB connection
client = None


#-----------------------------------------------------------
# Connect to the Turso DB and return the connection
#-----------------------------------------------------------
def connect_db():
    global client
    # Not connected yet?
    if client == None:
        # No, so make the connection to Turso
        client = create_client_sync(url=TURSO_URL, auth_token=TURSO_KEY)
    # Pass the connection back
    return client


#-----------------------------------------------------------
# Initialise the DB from the schema file
#-----------------------------------------------------------
def init_db(app):
    # Only initialise if developing locally (flask run --debug)
    if app.debug == True:
        # Connect to DB
        client = connect_db()
        # Open the DB schema and run
        with open(SCHEMA_FILE, "r") as f:
            client.execute(f.read())

