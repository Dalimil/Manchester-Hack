from flask import Flask
from flask import request, redirect, session, url_for, escape, make_response
import database
import rauth
import json
import os
from werkzeug import secure_filename
import random
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config( 
  cloud_name = "dhldfg16r", 
  api_key = "155162611414169", 
  api_secret = "E2SkhPl92ZV-Ojf4lfIbGOThC4w" 
)

# ---------------------------------------------

def get_results(params): # see Yelp API
  consumer_key = "NLcCQKXJM8VoQCm4IRktXQ"
  consumer_secret = "2-x1L5H-RdqWXZr21yrVgLD15Xk"
  token = "p3HHfCCvoeqCP7hefxJIKdV6GlY6kYjL"
  token_secret = "UFkGuY04zsHhDlOSlbj_FG9YW4g"
   
  session = rauth.OAuth1Session(
	consumer_key = consumer_key
	,consumer_secret = consumer_secret
	,access_token = token
	,access_token_secret = token_secret)
	 
  request = session.get("http://api.yelp.com/v2/search",params=params)
  data = request.json()
  session.close()

  parks = []
  field = ["id", "name", "distance", "snippet_text", "image_url", "location", "rating"]
  for p in data["businesses"]:
	parks.append({ f:p[f] for f in field if f in p })

  return {"parks": parks}

def get_search_parameters(lat,lng): 
  params = {} # see Yelp API
  params["category_filter"] = "parks"
  params["ll"] = "{},{}".format(str(lat),str(lng))
  params["radius_filter"] = "5000"
  return params

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in set(['png', 'jpg', 'jpeg'])


# -----------------------------------------------------

app = Flask(__name__)
# (session encryption) keep this really secret:
app.secret_key = "bnNoqxXSgzoXSOezxpZjb8mrMp5L0L4mJ4o8nRzn"

# SQL Alchemy database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/test.db' # absolute
# also possible "mysql://username:password@server/db" (or postgresql)
database.db.init_app(app) # bind
database.db.create_all(app=app) # create tables

# -----------------------------------------------------

@app.route('/')
def index():
	return """Use:<br> <b>GET /parks?lat=53.4723679&lng=-2.363677</b> to get Yelp data<br />
			<b> GET /pictures/park_id </b> to get images for the given park (e.g. try /pictures/park-3 )<br>
			<b> POST /add_picture</b> [img=file_object&name=pic_name&lat=53.4&lng=-2.3&park_id=default_park_id&user=contributing_user]<br>
			"""

@app.route('/parks')
def parks():
	lat = request.args.get('lat', 53.4723679)
	lng = request.args.get('lng', -2.363677)
	params = get_search_parameters(lat, lng)
	result = get_results(params)
	return json.dumps(result)

@app.route('/add_picture', methods=['POST'])
def add_picture():
	file = request.files['img']
	if file and allowed_file(file.filename):
		path = cloudinary.uploader.upload(file)
		path = path["url"]
		park_id = request.form['park_id'] or 'default_park_id'
		name = request.form['name'] or "my pic"
		lat = request.form['lat'] or 53.4723679
		lng = request.form['lng'] or -2.363677
		user = request.form['user'] or 'default'
		print(park_id, path, name, lat, lng, user)
		return "OK " + str(database.add_picture(park_id, path, name, lat, lng, user))

	abort(401)

@app.route('/pictures/<park_id>')
def get_pictures(park_id=None):
	return json.dumps(database.get_pictures(park_id)) 

@app.route('/debug')
def debug():
	return """<form action="/add_picture" enctype="multipart/form-data" method="post">
		<p>Park id:<br> <input type="text" name="park_id" size="30"></p>
		<p>Name:<br> <input type="text" name="name" size="30"></p>
		<p>Lat:<br> <input type="text" name="lat" size="30"></p>
		<p>Lng:<br> <input type="text" name="lng" size="30"></p>
		<p>User:<br> <input type="text" name="user" size="30"></p>
		<p>File:<br> <input type="file" name="img" size="40"></p>
		<input type="submit" value="Send">
		</form>
		"""
	# return str(database.add_picture("park-3", "filename.jpg", "fileXName", 50, -1, "def-user"))


if __name__ == '__main__':
	app.run(port=8080)#, debug=True)