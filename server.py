from pprint import pformat
import os

from jinja2 import StrictUndefined
import requests
from flask import Flask, render_template, request, flash, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"
app.jinja_env.undefined = StrictUndefined
# GOOGLE_KEY = os.environ['GOOGLE_KEY']
YELP_KEY = os.environ['YELP_API_KEY']
YELP_CLIENT = os.environ['CLIENT_ID']

@app.route("/")
def homepage():
	"""Show homepage"""

	return render_template("homepage.html")

@app.route("/city")
def show_top_sights():
	"""Show city's top sights"""

	city = request.args.get('city')

	# payload = {'location': 'city'}
	headers = {'Authorization': 'Bearer ' + YELP_KEY}

	r = requests.get('https://api.yelp.com/v3/businesses/search?term=Sightseeing&location=' + city, headers=headers)
	data = r.json()
	
	business = data["businesses"]


	for place in business:
		for info, value in place.items():
			print info, value
	

	

	return data



# @app.route("/map")
# def show_map():
#     return render_template("map.html")

# @app.route("/maps")
# def test_map():
#     return render_template("test_map.html")






if __name__ == "__main__":
	# We have to set debug=True here, since it has to be True at the
	# point that we invoke the DebugToolbarExtension
	app.debug = True
	app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
	# make sure templates, etc. are not cached in debug mode
	app.jinja_env.auto_reload = app.debug

	connect_to_db(app)

	# Use the DebugToolbar
	DebugToolbarExtension(app)

	app.run()