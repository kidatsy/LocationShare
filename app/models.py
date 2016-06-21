from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String)
    latitude = db.Column(db.String)
    longitude = db.Column(db.String)
    padding = db.Column(db.String)
    timestamp = db.Column(db.DateTime)

    def __init__(self,unique_id,padding,latitude,longitude,timestamp):
        self.unique_id = unique_id
        self.padding = padding
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = timestamp

