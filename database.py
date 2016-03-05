from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib
import json

db = SQLAlchemy()

def hash(data):
	return hashlib.sha256(str(data)).hexdigest()

class Picture(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	park_id = db.Column(db.Text)
	path = db.Column(db.Text, nullable = False)
	name = db.Column(db.String(40))
	lat = db.Column(db.Float)
	lng = db.Column(db.Float)
	user = db.Column(db.String(40))
	date_added = db.Column(db.DateTime)

	def __init__(self, park_id, path, name, lat, lng, user):
		self.park_id = park_id
		self.path = path
		self.name = name
		self.lat = lat
		self.lng = lng
		self.user = user
		self.date_added = datetime.utcnow()

	def getRepr(self): # fields = ["park_id", "path", "name", "lat", "lng", "user", "date_added"]
		return { "park_id": self.park_id, "path": self.path, "name": self.name, 
		"lat":self.lat, "lng":self.lng, "user": self.user, "date_added": str(self.date_added) }

	def __repr__(self):
		return json.dumps(self.getRepr())


# INSERT
def add_picture(park_id, path, name, lat, lng, user):
	new_pic = Picture(park_id, path, name, lat, lng, user)
	db.session.add(new_pic)
	db.session.commit()
	return new_pic.id

# QUERY
def get_pictures(park_id):
	objs =  Picture.query.filter_by(park_id=park_id).all()
	print(objs)
	return { "pictures": [ p.getRepr() for p in objs ] }
