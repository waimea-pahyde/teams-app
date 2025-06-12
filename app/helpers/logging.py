#===========================================================
# Error Related Functions
#===========================================================

from flask import request
import logging

# Disable built-in logging
logging.getLogger('werkzeug').setLevel(logging.CRITICAL)


#-----------------------------------------------------------
# Provide logging handlers to the Flask app
#-----------------------------------------------------------
def register_logging_handlers(app):

    @app.before_request
    def log_request():
        if app.debug and not '/static/' in request.path:
            print(f"\n + Request: {request.method} {request.path}")

            # Log the matched routing rule
            print(f"      Rule: {request.method} {request.url_rule}")

            if request.view_args:
                print(f"    Params: {request.view_args}")

            # Log the matched route function name
            print(f"   Handler: {request.endpoint}")

            if request.args:
                print(f"      Args: {request.args}")

            if request.form:
                print(f"      Form: {request.form}")

            if request.files:
                print(f"      File: {request.files}")

    @app.after_request
    def log_response(response):
        if app.debug:
            if not '/static/' in request.path:
                print(f"    Status: {response.status}\n")
            else:
                print(f" - Request: {request.method} {request.path} {response.status}")

            return response

