from pprint import pformat
import os

from jinja2 import StrictUndefined
import requests
from flask import Flask, render_template, request, flash, redirect, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Sight, Trip, Trip_sight

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
	"""Show city's top sights, with map and markers"""

	city = request.args.get('city')
	headers = {'Authorization': 'Bearer ' + YELP_KEY}

	r = requests.get('https://api.yelp.com/v3/businesses/search?term=Sightseeing&location=' + city, headers=headers)
	data = r.json()
	
	business = data["businesses"]

	top_sights = []
	coordinates = []
	image_url = []
	sight_url = []
	for place in business:
		for info, value in place.items():
			if info == "name":
				top_sights.append(value)
			elif info == "coordinates":
				coordinates.append(value)
			elif info == "image_url":
				image_url.append(value)
			elif info == "url":
				sight_url.append(value)

	region = data["region"]

	longitude = region["center"]["longitude"]
	latitude = region["center"]["latitude"]
	lat_long = {"lat": latitude, "lng": longitude}

	return jsonify(top_sights, lat_long, coordinates, image_url, sight_url)


@app.route('/register-form')
def register():
    """Show user register form"""

    return render_template("register_form.html")

@app.route('/registration', methods=['POST'])
def registration():
    """Registers user after submitting info"""

    user_email = request.form['email'].lower()
    user_password = request.form['password']
    user_fname = request.form['fname'].title()
    user_lname = request.form['lname'].title()

    email_query = User.query.filter_by(email=user_email).all()

    if email_query:
        return redirect("/login-form")

    else:
        user = User(fname=user_fname,
        			lname=user_lname,
        			email=user_email,
                    password=user_password)

        db.session.add(user)
        db.session.commit()

    return redirect("/login-form")

@app.route('/login-form')
def login_form():
    """Login form"""
    return render_template("login.html")

@app.route('/login', methods=["POST"])
def login_check():
    """Validates user info"""

    user_email = request.form['email']
    user_password = request.form['password']

    email_query = User.query.filter_by(email=user_email).first()

    if email_query == None:
    	flash('Invalid email, please Register')
        return redirect('/register-form')

    if user_password == email_query.password:

        session['user'] = email_query.user_id
        flash('You were successfully logged in')

        user_id = email_query.user_id

        return redirect('/')
    else:
        flash('Invalid email or password')
        return redirect('/login-form')

@app.route('/logout')
def logout():
    session.pop('user')
    flash('You were successfully logged out')

    return redirect('/')

@app.route('/trips')
def user_trips():
    """User's trips page, can add trip or view trips"""
    user_id = session['user']
    user = User.query.get(user_id)
    trips = Trip.query.order_by("city").all()

    return render_template("user_trips.html", user=user, trips=trips)

@app.route('/add-trips')
def add_trips():
	"""User adding a trip"""

        user = session['user']
	trip_name = request.args.get('trip').title()
        trip_city = Trip.query.filter_by(city=trip_name, user_id=user).all()
        trips=[]
        i=0
        while i < len(trip_city):
            trips.append(trip_city[i].city)
            i+=1
        if trip_name not in trips:
            trip = Trip(city=trip_name, user_id=user)
        else:
            return redirect('/trips')

	db.session.add(trip)
	db.session.commit()

	return redirect('/trips')

@app.route('/details/<trip>')
def trip_details(trip):
    """Detail for trip"""

    sights = Sight.query.all()

    return render_template("trip_info.html", sights=sights, trip=trip)

@app.route('/add-sights', methods=['POST'])
def add_sights():
    """Adding sights to a trip"""
    user_id = session['user']
    city = request.form.get('city')
    sight_name = request.form.get('sight_name')
    print sight_name
    sight = Sight(name_sight=sight_name, city=city, user_id=user_id)
    db.session.add(sight)
    db.session.commit()

    return "Success"


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

	app.run(port=5000, host='0.0.0.0')