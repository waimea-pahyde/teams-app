#===========================================================
# App Creation and Launch
#===========================================================

from flask import Flask, render_template, request, redirect
from supabase import create_client
from dotenv import load_dotenv
import os


# Load the Supabase API keys from the .env file
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create a Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Create the app
app = Flask(__name__)


#-----------------------------------------------------------
# Home page route - Show all the things, and new thing form
#-----------------------------------------------------------
@app.get("/")
def index():
    # Get all the things from the DB
    response = supabase.table("things").select().execute()
    records = response.data

    # Show the page with the DB data
    return render_template("pages/home.jinja", things=records)


#-----------------------------------------------------------
# Route for adding a thing, using data posted from a form
#-----------------------------------------------------------
@app.post("/add")
def add():
    # Get the data from the form
    name  = request.form["name"]
    price = request.form["price"]

    # Add the thing to the DB
    supabase.table("things").insert({
        "name": name,
        "price": price
    }).execute()

    # Go back to the home page
    return redirect("/")


#-----------------------------------------------------------
# Route for deleting a thing, Id given in the route
#-----------------------------------------------------------
@app.get("/delete/<int:itemId>")
def delete(itemId):
    # Delete the thing from the DB
    supabase.table("things").delete().eq("id", itemId).execute()

    # Go back to the home page
    return redirect("/")


#-----------------------------------------------------------
# About page route
#-----------------------------------------------------------
@app.get("/about")
@app.get("/about/")
def about():
    return render_template("pages/about.jinja")


#-----------------------------------------------------------
# 404 Error page
#-----------------------------------------------------------
@app.errorhandler(404)
def notFound(e):
    return render_template("pages/404.jinja")
