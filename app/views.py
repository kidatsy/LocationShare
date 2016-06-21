from app import app
from app.models import *
from app import db
import random
import json
from flask import request, render_template

def generate_id():
    unique_id = str(random.randint(10000,99999))
    while User.query.filter_by(unique_id=unique_id).count() > 0:
        unique_id = str(random.randint(10000,99999))
    padding = str(random.randint(10000,99999))
    user = User(unique_id,padding,'','')
    db.session.add(user)
    db.session.commit()
    return {"unique_id":unique_id,"padding":padding}

@app.route("/",methods=["GET","POST"])
def index():
    return "stubbed index"

@app.route("/send_url",methods=["GET"])
def send_url():
    dicter = generate_id()
    return "https://localhost:5000/"+dicter["unique_id"]+dicter["padding"]

@app.route("/get_location/<id>",methods=["GET","POST"])
def get_location(id):
    return render_template("get_location.html")
    
@app.route("/get_location_information",methods=["GET","POST"])
def get_location_information():
    #fill in the location information from the javascript
    jsdata = request.form["javascript_data"]
    jsdata = json.loads(jsdata)
    latitude = jsdata["latitude"]
    longitude = jsdata["longitude"]
    location_id = jsdata["location_id"]
    unique_id = location_id[:5]
    padding = location_id[5:]
    #I need a way to guarantee uniqueness, this will be a request to some other service internally
    #I can simulate this service
    #I should set up a foreign key so I can join on data from such a service
    #I don't know what this means? - this is guaranteed by generate_id...
    #maybe a redundant check isn't such a bad thing...
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
    return "successful"
