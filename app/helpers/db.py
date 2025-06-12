#===========================================================
# Database Related Functions
#===========================================================

from libsql_client import create_client_sync, LibsqlError
from contextlib import contextmanager
from dotenv import load_dotenv
from os import getenv, path


# Load Turso environment variables from the .env file
load_dotenv()
TURSO_URL = getenv("TURSO_URL")
TURSO_KEY = getenv("TURSO_KEY")

# Define the locations of our DB files
DB_FOLDER   = path.join(path.dirname(__file__), "db")
SCHEMA_FILE = path.join(DB_FOLDER, "schema.sql")


#-----------------------------------------------------------
# Connect to the Turso DB and return the connection
#-----------------------------------------------------------
@contextmanager
def connect_db():
    client = None

    try:
        client = create_client_sync(url=TURSO_URL, auth_token=TURSO_KEY)

        # Wrap the execute method to add logging
        original_execute = client.execute

        def logged_execute(sql, *args, **kwargs):
            from flask import current_app as app
            if app and app.debug:
                print(f"    DB SQL: {sql} | Params: {args if args else ''}")
            result = original_execute(sql, *args, **kwargs)
            if app and app.debug:
                print(f"      Rows: {getattr(result, 'rows', result)}")
            return result

        client.execute = logged_execute

        yield client

    finally:
        if client is not None:
            client.close()


