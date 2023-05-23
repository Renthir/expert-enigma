"""Server for Sci-fi TTRPG Character tracker"""

import os
from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db 
# from flask_login import LoginManager, login_required, logout_user, current_user
import crud

from jinja2 import StrictUndefined

# login_manager = LoginManager()

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined

# login_manager.init_app(app)


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


@app.route("/create-character", methods=["GET", "POST"])
def character_creator():
    """Page that allows for character creation"""
    #check session id for user's characters?
    if request.method == 'POST':
        return redirect(f"/characters")
        
    return render_template("character-creator.html")


@app.route("/character/<char_id>")
def character_details(char_id):
    """Shows character sheet, details, inventory"""
    return render_template("char_details.html")


# @app.route



if __name__ == "__main__":
    # connect_to_db(app)
    app.run(debug=True)