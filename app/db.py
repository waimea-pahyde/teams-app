#===========================================================
# Database Related Functions
#===========================================================

from libsql_client import create_client_sync
from contextlib import contextmanager
from dotenv import load_dotenv
import os


# Load Turso environment variables from the .env file
load_dotenv()
TURSO_URL = os.getenv("TURSO_URL")
TURSO_KEY = os.getenv("TURSO_KEY")

# Define the locations of our DB files
DB_FOLDER   = os.path.join(os.path.dirname(__file__), "db")
SCHEMA_FILE = os.path.join(DB_FOLDER, "schema.sql")


#-----------------------------------------------------------
# Connect to the Turso DB and return the connection
#-----------------------------------------------------------
@contextmanager
def connect_db():
    try:
        # Attempt to connect Turso DB, and pass back the connection
        client = create_client_sync(url=TURSO_URL, auth_token=TURSO_KEY)
        yield client

    except Exception as e:
        # Something went wrong!
        print(f"Database connection failed: {e}")
        yield None

    finally:
        # Properly close the connection when done
        if "client" in locals() and client is not None:
            client.close()


#-----------------------------------------------------------
# Initialise the DB from the schema file
#-----------------------------------------------------------
def init_db(app):
    # Only initialise if developing locally (flask run --debug)
    if app.debug == True:
        # Connect to DB
        with connect_db() as client:
            if client:
                try:
                    # Open the DB schema and run
                    with open(SCHEMA_FILE, "r") as f:
                        client.execute(f.read())

                except Exception as e:
                    # Something went wrong!
                    print(f"Database initialization failed: {e}")

            else:
                print("Database connection failed during initialization!")
