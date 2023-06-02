"""Scrip to seed DB"""

import os
import json
from random import choice, randint

import crud
import model
import server


server.app.app_context().push()

os.system("dropdb expert-enigma")
os.system("createdb expert-enigma")

model.connect_to_db(server.app)
model.db.create_all()

armors_data = [
    {"name": "Obsidian Assault Suit", "type": "Flack", "armor": 5, "price": 500},
    {"name": "Void-Walker Carapace", "type": "Powered", "armor": 15, "price": 2500},
    {"name": "Eclipse Vanguard", "type": "Exosuit", "armor": 10, "price": 1500}
]
weapons_data = [
    {"name": "Sand Caster", "type": "Macron", "dmg": 15, "range": 15, "price": 15000},
    {"name": "Quench-gun", "type": "Kinetic", "dmg": 4, "range": 250, "price": 500},
    {"name": "Lumin Rifle", "type": "Lasing", "dmg": 3, "range": 5000, "price": 5000}
]
background_data = [
    {"name": "Urchin", "desc": "Living on the streets in an urban world, you grew up fast and learned how to survive with little means. ", "rp": "You have a bonus to hiding in an urban environment, as well as to survival."},
    {"name": "Professor", "desc": "You've made your life in learning, received a good education and decided to pass on what you know, for one reason or another.", "rp": "You have a bonus to history and research rolls ."},
    {"name": "Mercenary", "desc": "A life of violence in exchange for cash. Maybe you justified it somehow, maybe you only took on contracts to defend the innocent. In any case, you've opted for a change. You do similar work now, but it's always for the innocent, and always for free. ", "rp": "ou get a bonus to strength and dexterity in combat."}
]

armors_db = []
for armor in armors_data:
    db_armor = crud.create_armor(armor_name=armor["name"], armor_type=armor["type"], armor_stat=armor['armor'], armor_price=armor["price"])
    armors_db.append(db_armor)
model.db.session.add_all(armors_db)
model.db.session.commit()

weapons_db = []
for weapon in weapons_data:
    db_weapon = crud.create_weapon(wep_name=weapon["name"], wep_type=weapon["type"], wep_dmg=weapon['dmg'], wep_range=weapon["range"], wep_price=weapon["price"])
    weapons_db.append(db_weapon)
model.db.session.add_all(weapons_db)
model.db.session.commit()

background_db = []
for back in background_data:
    db_background = crud.create_background(background_name=back["name"], descrip=back["desc"], rp_boon=back["rp"])
    background_db.append(db_background)
model.db.session.add_all(background_db)
model.db.session.commit()


for n in range(3):
    username = f"user{n}"
    password = "test"

    user = crud.create_user(username, password)
    model.db.session.add(user)

model.db.session.commit()
