"""CRUD Operations"""

from model import User, Character, Background, Inv_Armor, Armor, Inv_Wep, Weapon, connect_to_db

#creation functions

def create_user(username, password):
    user = User(username, password)
    return user

def create_char(char_name, user_id, background_id, bio, descrip):
    char = Character(char_name, user_id, background_id, bio, descrip)
    return char

def create_background(background_name, descrip, rp_boon):
    background = Background(background_name, descrip, rp_boon)
    return background

def create_weapon(wep_name, wep_dmg, wep_range, wep_price):
    weapon = Weapon(wep_name, wep_dmg, wep_range, wep_price)
    return weapon

def create_armor(armor_name, armor_stat, armor_price):
    armor = Armor(armor_name, armor_stat, armor_price)
    return armor

def create_inv_weapon(wep_id, char_id, qty):
    inv_weapon = Inv_Wep(wep_id, char_id, qty)
    return inv_weapon

def create_inv_armor(armor_id, char_id, qty):
    inv_armor = Inv_Armor(armor_id, char_id, qty)
    return inv_armor


# fetching functions

def get_armors():
    """Return all Armor"""
    return Armor.query.all()

def get_weapons():
    """Return all weapons"""
    return Weapon.query.all()

def get_characters(id):
    return Character.query.filter(Character.user_id == id).all()

def get_char_by_id(id):
    return Character.query.get(id)

def get_backgrounds():
    return Background.query.all()

def get_user_by_username(username):
    return User.query.filter(User.username == username).first()

def get_background_by_id(id):
    return Background.query.get(id)

def get_inventory(id):
    weps = Inv_Wep.query.filter(Inv_Wep.char_id == id).all()
    arms = Inv_Armor.query.filter(Inv_Armor.char_id == id).all()
    return weps, arms

#necesary junk
if __name__ == "__main__":
    from server import app
    connect_to_db(app)