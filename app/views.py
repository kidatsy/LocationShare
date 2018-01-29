from app import app
from app.models import *
from app import db
from app import login_manager
import random
from datetime import datetime, timedelta
import json
from flask import request, render_template, url_for,redirect,session,g
import flask_login as flask_login

#These routes are for logging in and out
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    email = request.form['email']
    password = request.form['pw']
    user = User.query.filter_by(email=email).first()
    if user:
        if user.password == password:
            flask_login.login_user(user,force=True)
            flask_login.current_user = user
            return redirect(url_for('show_db'))
    return 'Bad login'

@app.before_request
def before_request():
    g.user = flask_login.current_user
    
@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

#The following methods are all related to the show_db route aka the administrative dashboard
@app.route("/show_db",methods=["GET","POST"])
@flask_login.login_required
def show_db():
    locations = [to_geojson([elem.latitude,elem.longitude]) for elem in Clients.query.all() if elem.latitude != '' and elem.longitude != '']
    return render_template("show_db.html",results=Clients.query.all(),locations=json.dumps(locations))


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
    while Clients.query.filter_by(unique_id=unique_id).count() > 0:
        unique_id = str(random.randint(10000,99999))
    padding = str(random.randint(10000,99999))
    #This needs to be aware of the timezone of the User, instead of just doing datetime.now()
    user = Clients(unique_id,padding,'','',datetime.now(),"get_location/"+unique_id+padding,False)
    db.session.add(user)
    db.session.commit()
    return {"unique_id":unique_id,"padding":padding}

def to_geojson(coordinates):
    dicter = {}
    dicter["type"] = "Feature"
    dicter["properties"] = {}
    dicter["geometry"] = {
        "type":"Point",
        "coordinates":[float(coordinates[1]),float(coordinates[0])]
        }
    return dicter

@app.route("/delete_user",methods=["GET","POST"])
@flask_login.login_required
def delete_user():
    print("got here")
    user_id = request.form["user_id_to_delete"]
    if user_id.isdigit():
        user_to_delete = Clients.query.filter_by(unique_id=user_id)[0]
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
    return redirect(url_for("show_db"))

@app.route("/delete_all_users",methods=["GET","POST"])
@flask_login.login_required
def delete_all_users():
    two_days_ago = datetime.now() - timedelta(days=2)
    to_delete = db.session.query(User).filter(Clients.timestamp<two_days_ago).all()
    [db.session.delete(deleteable_element) for deleteable_element in to_delete]
    db.session.commit()
    return redirect(url_for("show_db"))
        
@app.route("/send_url",methods=["GET"])
@flask_login.login_required
def send_url():
    dicter = generate_id()
    return json.dumps({"url":"get_location/"+dicter["unique_id"]+dicter["padding"]})

@app.route("/get_location/<id>",methods=["GET","POST"])
def get_location(id):
    return render_template("get_location.html")

@app.route("/map_view/<unique_id>",methods=["GET","POST"])
@flask_login.login_required
def map_view(unique_id):
    user = Clients.query.filter_by(unique_id=unique_id).first()
    location = to_geojson([user.latitude,user.longitude])
    return render_template("map_view.html",locations=json.dumps([location]))


@app.route("/post_location_information",methods=["POST"])
def post_location_information():
    jsdata = request.form["javascript_data"]
    jsdata = json.loads(jsdata)
    latitude = jsdata["latitude"]
    longitude = jsdata["longitude"]
    location_id = jsdata["location_id"]
    unique_id = location_id[:5]
    padding = location_id[5:]
    
    try:
        user = Clients.query.filter_by(unique_id=unique_id).all()[0]
    except IndexError:
        #if for some reason there was no user id generated, a user id is generated now
        #This needs to be aware of the timezone of the User, instead of just doing datetime.now()
        user = Clients(unique_id,padding,'','',datetime.now(),"get_location/"+unique_id+padding,True)
        db.session.add(user)
        db.session.commit()
        return "successful"
    user.latitude = latitude
    user.longitude = longitude
    user.timestamp = datetime.now()
    user.link_clicked = True
    db.session.add(user)
    db.session.commit()
    return "successful"
