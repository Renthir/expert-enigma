"""Server for Sci-fi TTRPG Character tracker"""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db 
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined


# Routes

@app.route("/")
def homepage():
    """View homepage"""
    return render_template("home.html")


# @app.route("/login")
# def login():


@app.route("/armors")
def armors_page():
    """View Armor list"""
    return render_template("armors.html")

@app.route("/weapons")
def weapons_page():
    """View Weapons list"""
    return render_template("weapons.html")

@app.route("/characters")
def characters_page():
    """Page that shows a user's characters and the option to create a new one"""
    #check session id to see if user is logged in, provide user's characters
    return render_template("characters.html")


