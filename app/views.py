from app import app
from app.models import *
from app import db
import random
import json
from flask import request

def generate_id():
    unique_id = str(random.randint(10000,99999))
    while User.query.filter_by(unique_id=unique_id).count() > 0:
        unique_id = str(random.randint(10000,99999))
    padding = str(random.randint(10000,99999))
    user = User(unique_id,padding,'','')
    db.session.add(user)
    db.session.commit()
    return {"unique_id":unique_id,"padding":padding}

@app.route("/send_url",methods=["GET"])
def send_url():
    dicter = generate_id()
    return "https://localhost:5000/"+dicter["unique_id"]+dicter["padding"]

@app.route("/get_location/<int:id>",methods=["GET","POST"])
def get_location(id):
    #fill in the location information from the javascript
    latitude = "00000"
    longitude = "00000"
    unique_id = id[:5]
    padding = id[5:]
    #I need a way to guarantee uniqueness, this will be a request to some other service internally
    #I can simulate this service
    #I should set up a foreign key so I can join on data from such a service
    try:
        user = User.query.filter_by(unique_id=unique_id).all()[0]
    except IndexError:
        user = User(unique_id,padding,'','')
        db.session.add(user)
        db.session.commit()
    user.latitude = latitude
    user.longitude = longitude
    db.session.add(user)
    db.session.commit()
    
