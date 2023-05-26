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
    {"name": "Flack", "armor": 5, "price": 500},
    {"name": "Carapace", "armor": 10, "price": 1000}
]
weapons_data = [
    {"name": "Sand Caster", "dmg": 15, "range": 10, "price": 15000},
    {"name": "Kinetic Rifle", "dmg": 2, "range": 200, "price": 250}
]
background_data = [
    {"name": "Urchin", "desc": "Grew up on the streets", "rp": "Advantage to survival roles"},
    {"name": "Professor", "desc": "Had tenure at a university", "rp": "Advantage to history checks"}
]

armors_db = []
for armor in armors_data:
    db_armor = crud.create_armor(armor_name=armor["name"], armor_stat=armor['armor'], armor_price=armor["price"])
    armors_db.append(db_armor)
model.db.session.add_all(armors_db)
model.db.session.commit()

weapons_db = []
for weapon in weapons_data:
    db_weapon = crud.create_weapon(wep_name=weapon["name"], wep_dmg=weapon['dmg'], wep_range=weapon["range"], wep_price=weapon["price"])
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
