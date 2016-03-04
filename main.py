from flask import Flask
from flask import request, redirect, session, url_for, escape, make_response, flash, abort
import database
import rauth
import json

app = Flask(__name__)
# (session encryption) keep this really secret:
app.secret_key = "bnNoqxXSgzoXSOezxpZjb8mrMp5L0L4mJ4o8nRzn"

# SQL Alchemy database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db' # absolute
# also possible "mysql://username:password@server/db" (or postgresql)
database.db.init_app(app) # bind
database.db.create_all(app=app) # create tables

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

@app.route('/')
def index():
	params = get_search_parameters(53.4723679, -2.363677)
	result = get_results(params)
	return json.dumps(result)

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