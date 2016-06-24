from app import app
from app.models import *
from app import db
import random
from datetime import datetime, timedelta
import json
from flask import request, render_template

def generate_id():
    """
    This method generates a unique id that does not currently exist in our database.
    
    This function takes no parameters
    
    This function returns a dictionary with the following keys:
    
    @unique_id - a unique number that we are guaranteed does not already exist in our database at request time

    @padding - a randomly generated number that we more or less don't care about and is only there to prevent attackers
    We restrict ourselves to a unique id with 5 digits for a few reasons:
    1. We wipe our database every 48 hours
    2. This only a prototype application
    Should this change the get_location_information() function will need to change as well,
    because it currently explicitly expects padding of 5 random digits and 5 digits that will form the unique_id
    """
    unique_id = str(random.randint(10000,99999))
    while User.query.filter_by(unique_id=unique_id).count() > 0:
        unique_id = str(random.randint(10000,99999))
    padding = str(random.randint(10000,99999))
    #This needs to be aware of the timezone of the User, instead of just doing datetime.now()
    user = User(unique_id,padding,'','',datetime.now())
    db.session.add(user)
    db.session.commit()
    return {"unique_id":unique_id,"padding":padding}

def to_geojson(coordinates):
    print("coordinates",coordinates)
    dicter = {}
    dicter["type"] = "Feature"
    dicter["properties"] = {}
    dicter["geometry"] = {
        "type":"Point",
        "coordinates":[float(coordinates[0]), float(coordinates[1])]
        }
    return dicter

@app.route("/",methods=["GET","POST"])
def index():
    return "stubbed index"

@app.route("/delete_user",methods=["GET","POST"])
def delete_user():
    user_id = request.form["user_id"]
    if user_id.isdigit():
        user_to_delete = User.query.filter_by(unique_id=user_id)[0]
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
        return "successful"
    else:
        return "failure"

@app.route("/delete_all_users",methods=["GET","POST"])
def delete_all_users():
    two_days_ago = datetime.now() - timedelta(days=2)
    to_delete = db.session.query(User).filter(User.timestamp<two_days_ago).all()
    [db.session.delete(deleteable_element) for deleteable_element in to_delete]
    db.session.commit()
    return "successful"
        
@app.route("/send_url",methods=["GET"])
def send_url():
    dicter = generate_id()
    return "http://localhost:5000/get_location/"+dicter["unique_id"]+dicter["padding"]

@app.route("/get_location/<id>",methods=["GET","POST"])
def get_location(id):
    return render_template("get_location.html")

@app.route("/map_view/<unique_id>",methods=["GET","POST"])
def map_view(unique_id):
    print("unique_id",unique_id)
    user = User.query.filter_by(unique_id=unique_id).first()
    locations = to_geojson([user.latitude,user.longitude])
    return render_template("map_view.html",locations=json.dumps(locations))

@app.route("/show_db",methods=["GET","POST"])
def show_db():
    return render_template("show_db.html",results=User.query.all())

@app.route("/get_location_information",methods=["GET","POST"])
def get_location_information():
    jsdata = request.form["javascript_data"]
    jsdata = json.loads(jsdata)
    latitude = jsdata["latitude"]
    longitude = jsdata["longitude"]
    location_id = jsdata["location_id"]
    unique_id = location_id[:5]
    padding = location_id[5:]
    
    try:
        user = User.query.filter_by(unique_id=unique_id).all()[0]
    except IndexError:
        #if for some reason there was no user id generated, a user id is generated now
        #This needs to be aware of the timezone of the User, instead of just doing datetime.now()
        user = User(unique_id,padding,'','',datetime.now())
        db.session.add(user)
        db.session.commit()
    user.latitude = latitude
    user.longitude = longitude
    user.timestamp = datetime.now()
    db.session.add(user)
    db.session.commit()
    return "successful"
