from app import db
import flask.ext.login as flask_login

class User(db.Model,flask_login.UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String,unique=True)
    password = db.Column(db.String) #this should be changed to a hash

    def get_id(self):
        return str(self.id)
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __init__(self,email,password):
        self.email = email
        self.password = password
    
class Clients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String)
    latitude = db.Column(db.String)
    longitude = db.Column(db.String)
    padding = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
    url = db.Column(db.String)

    def __init__(self,unique_id,padding,latitude,longitude,timestamp,url):
        self.unique_id = unique_id
        self.padding = padding
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = timestamp
        self.url = url

