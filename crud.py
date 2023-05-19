"""CRUD Operations"""

from model import User, Character, Background, Inv_Armor, Armor, Inv_Wep, Weapon

#functions

def create_user(email, password):
    user = User(email=email, password=password)
    return user

def create_char(char_name, user_id, background_id, bio, descrip):
    char = Character(char_name=char_name, user_id=user_id, background_id=background_id, bio=bio, descrip=descrip)
    return Character

def create_background(background_name, descrip, rp_boon):
    background = Background(background_name=background_name, descrip=descrip, rp_boon=rp_boon)
    return background

def create_weapon(wep_name, wep_dmg, wep_range, wep_price):
    weapon = Weapon(wep_name=wep_name, wep_dmg=wep_dmg, wep_range=wep_range, wep_price=wep_price)
    return weapon

def create_armor(armor_name, armor_stat, armor_price):
    armor = Armor(armor_name=armor_name, armor_stat=armor_stat, armor_price=armor_price)
    return armor

