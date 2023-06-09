"""Server for Sci-fi TTRPG Character tracker"""

import os
from flask import Flask, render_template, request, flash, session, redirect, url_for
from model import connect_to_db, db, User 
from flask_login import LoginManager, login_required, logout_user, current_user, login_user
import crud

from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined
app.debug = True

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
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()

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
    username = request.form.get("username")
    password = request.form.get("password")
    user = crud.get_user_by_username(username)
    if user:
        flash("Username already taken")
    else:
        user = crud.create_user(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")
    return redirect("/")


@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    flash("Log Out Successful")
    return redirect("/")


@app.route("/armors", methods=["GET", "POST"])
@login_required
def armors_page():
    """View Armor list"""
    armors = crud.get_armors()
    chars = crud.get_characters(current_user.user_id)

    if request.method == "POST":
        char_id = request.form.get("character")
        armor_id = request.form.get("armor")

        inv_armor = crud.create_inv_armor(armor_id, int(char_id))
        db.session.add(inv_armor)
        db.session.commit()
        flash("Armor Added!")

    return render_template("armors.html", armors=armors, characters=chars)


@app.route("/weapons", methods=["GET", "POST"])
@login_required
def weapons_page():
    """View Weapons list"""
    weapons = crud.get_weapons()
    chars = crud.get_characters(current_user.user_id)

    if request.method == "POST":
        char_id = request.form.get("character")
        wep_id = request.form.get("weapon")

        inv_wep = crud.create_inv_weapon(wep_id, int(char_id))
        db.session.add(inv_wep)
        db.session.commit()
        flash("Weapon Added!")
    
    return render_template("weapons.html", weapons=weapons, characters=chars)


@app.route("/characters")
@login_required
def characters_page():
    """Page that shows a user's characters and the option to create a new one"""
    characters = crud.get_characters(current_user.user_id)
    return render_template("characters.html", characters=characters)


@app.route("/create-character", methods=["GET", "POST"])
@login_required
def character_creator():
    """Page that allows for character creation"""
    backgrounds = crud.get_backgrounds()

    if request.method == 'POST':
        name = request.form.get("name")
        desc = request.form.get("description")
        bio = request.form.get("bio")
        background = request.form.get("background") 
        print(background)

        char = crud.create_char(name, current_user.user_id, int(background), bio, desc)
        db.session.add(char)
        db.session.commit()

        flash("Character created!")
        return redirect(f"/characters")
        
    return render_template("character-creator.html", backgrounds=backgrounds)


@app.route("/character/<char_id>")
@login_required
def character_details(char_id):
    """Shows character sheet, details, inventory"""
    char = crud.get_char_by_id(char_id)
    back = crud.get_background_by_id(char.background_id)
    weapons, armors = crud.get_inventory(char_id)

    if char.user_id != current_user.user_id:
        flash("Invalid Character Page")
        return redirect("/characters")
    return render_template("char-details.html", character=char, background=back, armors=armors, weapons=weapons)


@app.route("/character/<char_id>/edit", methods=["GET", "POST"])
@login_required
def edit_character(char_id):
    char = crud.get_char_by_id(char_id)
    backgrounds = crud.get_backgrounds()
    #finish edit
    if char.user_id != current_user.user_id:
        flash("Invalid Request")
        return redirect("/characters")
    
    if request.method == "POST":
        name = request.form.get("name")
        desc = request.form.get("description")
        bio = request.form.get("bio")
        background = request.form.get("background") 

        # char = crud.create_char(name, current_user.user_id, int(background), bio, desc)
        char.char_name = name
        char.descrip = desc
        char.bio = bio
        char.background = int(background)
        db.session.commit()

    return render_template("edit-character.html", character=char, backgrounds=backgrounds)


@app.route("/admin")
@login_required
def admin():
    if not current_user.check_admin():
        flash("Not Authorized")
        return redirect("/")
    return render_template("admin-forms.html")


@app.route("/delete_arm/<char_id>/<armor_id>")
@login_required
def delete_inv_armor(char_id, armor_id):
    char = crud.get_char_by_id(char_id)
    inv_armor = crud.get_inv_armor(char_id, armor_id)
    
    if char.user_id != current_user.user_id:
        flash("Invalid Request")
        return redirect("/characters")
    
    if inv_armor:
        db.session.delete(inv_armor)
        db.session.commit()

    flash("Item Deleted")
    return redirect(url_for('character_details', char_id=char_id))

@app.route("/delete_wep/<char_id>/<wep_id>")
@login_required
def delete_inv_wep(char_id, wep_id):
    char = crud.get_char_by_id(char_id)
    inv_wep = crud.get_inv_wep(char_id, wep_id)

    if char.user_id != current_user.user_id:
        flash("Invalid Request")
        return redirect("/characters")
    
    if inv_wep:
        db.session.delete(inv_wep)
        db.session.commit()
    
    
    flash("Item Deleted")
    return redirect(url_for('character_details', char_id=char_id))


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)