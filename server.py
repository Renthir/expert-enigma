"""Server for Sci-fi TTRPG Character tracker"""

import os
from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db, User 
from flask_login import LoginManager, login_required, logout_user, current_user, login_user
import crud

from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Routes

@app.route("/")
def homepage():
    """View homepage"""
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.filter_by(email=email).first()

    if request.method == 'POST':
        if user:
            if user.check_password(password):
                login_user(user)
                flash("Login Successful!")
                return redirect("/")
            else:
                flash("Invalid login information")
                return redirect("/login")
        else:
            flash("Invalid login information")
            return redirect("/login")
        
    return render_template("reg-login.html")


@app.route("/register", methods=["POST"])
def register():
    return redirect("/")

@app.route("/armors")
def armors_page():
    """View Armor list"""
    armors = crud.get_armors()
    return render_template("armors.html", armors=armors)

@app.route("/logout", methods=["POST"])
def logout():

    flash("Log Out Successful")
    return redirect("/")

@app.route("/weapons")
def weapons_page():
    """View Weapons list"""
    weapons = crud.get_weapons()
    return render_template("weapons.html", weapons=weapons)


@app.route("/characters")
@login_required
def characters_page():
    """Page that shows a user's characters and the option to create a new one"""
    characters = crud.get_characters(current_user.user_id)
    return render_template("characters.html", characters=characters)


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

@app.route("/admin")
@login_required
def admin():
    if not current_user.check_admin():
        flash("Not Authorized")
        return redirect("/")
    return render_template("admin-forms.html")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)