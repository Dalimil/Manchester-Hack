from flask import Flask
from flask import request, redirect, session, url_for, escape, make_response, flash, abort
import database

app = Flask(__name__)
# (session encryption) keep this really secret:
app.secret_key = "bnNoqxXSgzoXSOezxpZjb8mrMp5L0L4mJ4o8nRzn"

# SQL Alchemy database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db' # absolute
# also possible "mysql://username:password@server/db" (or postgresql)
database.db.init_app(app) # bind
database.db.create_all(app=app) # create tables

@app.route('/')
def index():
	return "all ok"

@app.route('/create_user', methods=['POST'])
def create_user():
	# database.add_user(name, "1234-"+name)
	return "created"

@app.route('/user/<name>')
def get_user(name=None):
	# name is a variable obtained from the url path
	print(database.get_users()) 
	return "Bob"


if __name__ == '__main__':
	#host='0.0.0.0' only with debug disabled - security risk
	app.run(port=8080, debug=True)