from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib

db = SQLAlchemy()

def hash(data):
	return hashlib.sha256(str(data)).hexdigest()

class Picture(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	path = db.Column(db.Text, nullable = False)
	name = db.Column(db.String(40))
	lat = db.Column(db.Float)
	lng = db.Column(db.Float)
	user = db.Column(db.String(40))
	date_added = db.Column(db.DateTime)

	def __init__(self, path, name, lat, lng, user):
		self.path = path
		self.name = name
		self.lat = lat
		self.lng = lng
		self.user = user
		self.date_added = date_added
		self.date_added = datetime.utcnow()

# INSERT
def add_picture(path, name, lat, lng, user):
	new_pic = Picture(path, name, lat, lng, user)
	db.session.add(new_pic)
	db.session.commit()
	print(new_pic.id)

# QUERY
def get_pictures(park_id):
	return Picture.query.filter_by(park_id=park_id).all()
