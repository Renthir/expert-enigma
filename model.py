"""Data tables for users and characters, their items"""

import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

#Class tables

class User(db.Model, UserMixin):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    is_admin = db.Column(db.Boolean)

    characters = db.relationship("Character", backref="users", lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.is_admin = False

    def __repr__(self):
        return f"<User user_id={self.user_id} username={self.username}>"
    
    def get_id(self):
        return self.user_id
    
    def check_password(self, password):
        return password == self.password
    
    def check_admin(self):
        return self.is_admin
    

class Character(db.Model):
    __tablename__ = 'characters'

    char_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    char_name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    background_id = db.Column(db.Integer, db.ForeignKey("backgrounds.background_id"))
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
    background_name = db.Column(db.String, unique=True)
    descrip = db.Column(db.Text)
    rp_boon = db.Column(db.Text)

    def __init__(self, background_name, descrip, rp_boon):
        self.background_name = background_name
        self.descrip = descrip
        self.rp_boon = rp_boon

    def __repr__(self):
        return f"<Background background_id={self.user_id} background_name={self.background_name}>"


class Weapon(db.Model):
    __tablename__ = 'weapons'

    wep_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    wep_name = db.Column(db.String, unique=True)
    wep_type = db.Column(db.String)
    wep_dmg = db.Column(db.Integer)
    wep_range = db.Column(db.Integer)
    wep_price = db.Column(db.Integer)

    def __init__(self, wep_name, wep_type, wep_dmg, wep_range, wep_price):
        self.wep_name = wep_name
        self.wep_type = wep_type
        self.wep_dmg = wep_dmg
        self.wep_range = wep_range
        self.wep_price = wep_price

    def __repr__(self):
        return f"<Weapon wep_id={self.wep_id} wep_name={self.wep_name}>"
    

class Armor(db.Model):
    __tablename__ = 'armors'

    armor_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    armor_name = db.Column(db.String, unique=True)
    armor_type = db.Column(db.String)
    armor_stat = db.Column(db.Integer)
    armor_price = db.Column(db.Integer)

    def __init__(self, armor_name, armor_type, armor_stat, armor_price):
        self.armor_name = armor_name
        self.armor_type = armor_type
        self.armor_stat = armor_stat
        self.armor_price = armor_price
    def __repr__(self):
        return f"<Armor armor_id={self.armor_id} armor_name={self.armor_name}>"


class Inv_Wep(db.Model):
    __tablename__ = 'inv_weapons'

    inv_wep_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    wep_id = db.Column(db.Integer, db.ForeignKey("weapons.wep_id"))
    char_id = db.Column(db.Integer, db.ForeignKey("characters.char_id"))
    qty = db.Column(db.Integer)
    is_equipped = db.Column(db.Boolean)

    def __init__(self, wep_id, char_id):
        self.wep_id = wep_id
        self.char_id = char_id
        self.qty = 1
        self.is_equipped = False

    def __repr__(self):
        return f"<Inv_wep id={self.inv_wep_id}>"


class Inv_Armor(db.Model):
    __tablename__ = 'inv_armors'

    inv_armor_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    armor_id = db.Column(db.Integer, db.ForeignKey("armors.armor_id"))
    char_id = db.Column(db.Integer, db.ForeignKey("characters.char_id"))
    qty = db.Column(db.Integer)
    is_equipped = db.Column(db.Boolean)

    def __init__(self, armor_id, char_id):
        self.armor_id = armor_id
        self.char_id = char_id
        self.qty = 1
        self.is_equipped = False


    def __repr__(self):
        return f"<Inv_Armor id={self.inv_armor_id}>"


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
