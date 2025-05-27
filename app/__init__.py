#===========================================================
# App Creation and Launch
#===========================================================

from flask import Flask, render_template, request, redirect
from app.db import init_db, connect_db

# Create the app
app = Flask(__name__)

# Setup the database
init_db(app)


#-----------------------------------------------------------
# Home page route - Show all the things, and new thing form
#-----------------------------------------------------------
@app.get("/")
def index():
    # Get all the things from the DB
    client = connect_db()
    result = client.execute("SELECT * FROM things")

    # Show the page with the DB data
    return render_template("pages/home.jinja", things=result.rows)


#-----------------------------------------------------------
# Route for adding a thing, using data posted from a form
#-----------------------------------------------------------
@app.post("/add")
def add():
    # Get the data from the form
    name  = request.form["name"]
    price = request.form["price"]

    # Add the thing to the DB
    client = connect_db()
    client.execute("INSERT INTO things (name, price) VALUES (?, ?)", [name, price])

    # Go back to the home page
    return redirect("/")


#-----------------------------------------------------------
# Route for deleting a thing, Id given in the route
#-----------------------------------------------------------
@app.get("/delete/<int:itemId>")
def delete(itemId):
    # Delete the thing from the DB
    client = connect_db()
    client.execute("DELETE FROM things WHERE id=?", [itemId])

    # Go back to the home page
    return redirect("/")


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
def notFound(e):
    return render_template("pages/404.jinja")
