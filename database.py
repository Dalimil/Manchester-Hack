from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib

db = SQLAlchemy()

def hash(data):
	return hashlib.sha256(str(data)).hexdigest()

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), unique=True)
	password = db.Column(db.Text, nullable=False)
	
	# types are: Integer, String(maxLen), Text, DateTime, Float, PickleType, LargeBinary
	# relationships: http://flask-sqlalchemy.pocoo.org/2.1/models/

	def __init__(self, username, password):
		self.username = username
		self.password = hash(password)
		

class Picture(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.Text, nullable = False)
	date_added = db.Column(db.DateTime)

	def __init__(self, url, date_added):
		self.url = url
		self.date_added = datetime.utcnow()


# INSERT
def add_user(username, password):
	new_user = User('guest', '123456789')
	db.session.add(new_user) # delete works similarly
	db.session.commit()
	print(new_user.id)

# QUERY
def get_users():
	users = User.query.all()
	# More examples:
	guest = User.query.filter_by(username='guest').first()
	if guest != None:
		print(guest.username)

	User.query.filter(User.username.endswith('st')).order_by(User.username).limit(2).all()
	primary_key = 1
	User.query.get(primary_key)

	return users
