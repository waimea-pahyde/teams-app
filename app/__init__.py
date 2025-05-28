#===========================================================
# App Creation and Launch
#===========================================================

from flask import Flask, render_template, request, redirect
from app.db import init_db, connect_db
import html
import traceback


# Create the app
app = Flask(__name__)

# Setup the database
init_db(app)


#-----------------------------------------------------------
# Home page route - Show all the things, and new thing form
#-----------------------------------------------------------
@app.get("/")
def index():
    with connect_db() as client:
        if client:
            try:
                # Get all the things from the DB and show on page
                result = client.execute("SELECT * FROM things")
                return render_template("pages/home.jinja", things=result.rows)

            except Exception:
                print("Error fetching data")
                return server_error("Error fetching data from the database")
        else:
            return server_error("Database connection failed")


#-----------------------------------------------------------
# Route for adding a thing, using data posted from a form
#-----------------------------------------------------------
@app.post("/add")
def add():
    # Get the data from the form
    name  = request.form.get("name")
    price = request.form.get("price")

    # Sanitise the inputs
    name = html.escape(name)
    price = html.escape(price)

    with connect_db() as client:
        if client:
            try:
                # Add the thing to the DB
                client.execute("INSERT INTO things (name, price) VALUES (?, ?)", [name, price])
                # Go back to the home page
                return redirect("/")

            except Exception:
                print(f"Error inserting data - name:{name}, price:{price}")
                return server_error("Error adding data to the database")
        else:
            return server_error("Database connection failed")


#-----------------------------------------------------------
# Route for deleting a thing, Id given in the route
#-----------------------------------------------------------
@app.get("/delete/<int:itemId>")
def delete(itemId):
    with connect_db() as client:
        if client:
            try:
                # Delete the thing from the DB
                client.execute("DELETE FROM thingss WHERE id=?", [itemId])
                # Go back to the home page
                return redirect("/")

            except Exception:
                print(f"Error deleting item - id:{itemId}")
                return server_error("Error deleting item from the database")
        else:
            return server_error("Database connection failed")


#-----------------------------------------------------------
# About page route
#-----------------------------------------------------------
@app.get("/about")
def about():
    return render_template("pages/about.jinja")


#-----------------------------------------------------------
# 404 Error page
#-----------------------------------------------------------
@app.errorhandler(404)
def not_found(e):
    return render_template("pages/404.jinja")


#-----------------------------------------------------------
# 500 Error page
#-----------------------------------------------------------
@app.errorhandler(500)
def server_error(e):
    return render_template("pages/500.jinja", error=str(e)), 500
