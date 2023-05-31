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

def create_weapon(wep_name, wep_type, wep_dmg, wep_range, wep_price):
    weapon = Weapon(wep_name, wep_type, wep_dmg, wep_range, wep_price)
    return weapon

def create_armor(armor_name, armor_type, armor_stat, armor_price):
    armor = Armor(armor_name, armor_type, armor_stat, armor_price)
    return armor

def create_inv_weapon(wep_id, char_id):
    inv_weapon = Inv_Wep(wep_id, char_id)
    return inv_weapon

def create_inv_armor(armor_id, char_id):
    inv_armor = Inv_Armor(armor_id, char_id)
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
    inv_weps = Inv_Wep.query.filter(Inv_Wep.char_id == id).all()
    inv_arms = Inv_Armor.query.filter(Inv_Armor.char_id == id).all()

    weps = []
    for inv_wep in inv_weps:
        weps.append(Weapon.query.filter(Weapon.wep_id == inv_wep.wep_id).first())

    arms = []
    for inv_armor in inv_arms:
        arms.append(Armor.query.filter(Armor.armor_id == inv_armor.armor_id).first())

    return weps, arms

def get_inv_armor(char_id, armor_id):
    armor = Inv_Armor.query.filter(Inv_Armor.char_id == char_id and Inv_Armor.armor_id == armor_id).first()
    return armor

def get_inv_wep(char_id, wep_id):
    weapon = Inv_Wep.query.filter(Inv_Wep.char_id == char_id and Inv_Wep.wep_id == wep_id).first()
    return weapon


#necesary junk
if __name__ == "__main__":
    from server import app
    connect_to_db(app)