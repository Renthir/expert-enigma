"""Data tables for users and characters, their items"""

import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

#Class tables

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"
    

class Character(db.Model):
    __tablename__ = 'characters'

    char_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    char_name = db.Column(db.String)
    # user_id = db.Column(db.Integer)
    # background_id = db.Column(db.Integer)
    bio = db.Column(db.Text)
    descrip = db.Column(db.Text)

    def __init__(self, char_name, user_id, background_id, bio, descrip):
        self.char_name = char_name
        self.user_id = user_id
        self.background_id = background_id
        self.bio = bio
        self.descrip = descrip
    
    def __repr__(self):
        return f"<Character char_id={self.char_id} char_name={self.char_name}>"
    

class Background(db.Model):
    __tablename__ = 'backgrounds'

    background_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    back_name = db.Column(db.String, unique=True)
    descrip = db.Column(db.Text)

    def __init__(self, back_name, descrip):
        self.back_name = back_name
        self.descrip = descrip

    def __repr__(self):
        return f"<Background background_id={self.user_id} back_name={self.back_name}>"


class Weapon(db.Model):
    __tablename__ = 'weapons'

    wep_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    wep_name = db.Column(db.String, unique=True)
    wep_dmg = db.Column(db.Integer)
    wep_range = db.Column(db.Integer)
    wep_price = db.Column(db.Integer)

    def __init__(self, wep_name, wep_dmg, wep_range, wep_price):
        self.wep_name = wep_name
        self.wep_dmg = wep_dmg
        self.wep_range = wep_range
        self.wep_price = wep_price

    def __repr__(self):
        return f"<Weapon wep_id={self.wep_id} wep_name={self.wep_name}>"
    

class Armor(db.Model):
    __tablename__ = 'armors'

    armor_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    armor_name = db.Column(db.String, unique=True)
    armor_stat = db.Column(db.Integer)
    armor_price = db.Column(db.Integer)

    def __init__(self, armor_name, armor_stat, armor_price):
        self.armor_name = armor_name
        self.armor_stat = armor_stat
        self.armor_price = armor_price
    def __repr__(self):
        return f"<Armor armor_id={self.armor_id} armor_name={self.armor_name}>"




# Other necessities

def connect_to_db(flask_app):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
