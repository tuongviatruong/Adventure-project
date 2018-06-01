from pprint import pformat
import os

from jinja2 import StrictUndefined
import requests
from flask import Flask, render_template, request, flash, redirect, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Sight, Trip, Trip_sight
from sqlalchemy import update

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

    r = requests.get('https://api.yelp.com/v3/businesses/search?term=Tourist+Attractions&location=' + city, headers=headers)
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

    if session:
        user_id = session['user']
        trips_query = Trip.query.filter_by(user_id=user_id).all()
        trips=[]
        i=0
        while i < len(trips_query):
            trips.append(trips_query[i].trip_name)
            i+=1
        return jsonify(top_sights, lat_long, coordinates, image_url, sight_url, trips)
    else:
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

        return redirect('/trips')
    else:
        flash('Invalid email or password')
        return redirect('/login-form')

@app.route('/logout')
def logout():

    del session["user"]
    flash('You were successfully logged out')

    return redirect('/')

@app.route('/trips')
def user_trips():
    """User's trips page, can add trip or view trips"""
    user_id = session['user']
    user = User.query.get(user_id)
    trips = Trip.query.order_by("trip_name").all()

    return render_template("user_trips.html", user=user, trips=trips)

@app.route('/add-trips')
def add_trips():
    """User adding a trip"""

    user = session['user']
    trip_name = request.args.get('trip').title().strip()
    trip_query = Trip.query.filter_by(trip_name=trip_name, user_id=user).all()

    trips=[]
    i=0
    while i < len(trip_query):
        trips.append(trip_query[i].trip_name)
        i+=1

    if trip_name not in trips:
        trip = Trip(trip_name=trip_name, user_id=user)
    else:
        return redirect('/trips')

    db.session.add(trip)
    db.session.commit()

    return redirect('/trips')

@app.route('/details/<trip>')
def trip_details(trip):
    """Detail for trip"""

    user = session['user']
    trip_query = Trip.query.filter_by(trip_name=trip, user_id=user).all()
    trip_id = trip_query[0].trip_id
    trip_sights_query = Trip_sight.query.filter_by(trip_id=trip_id).all()

    return render_template("trip_info.html", sights=trip_sights_query, trip=trip)

@app.route('/add-sights', methods=['POST'])
def add_sights():
    """Adding sights to a trip"""

    user_id = session['user']
    city = request.form.get('city').title()

    sight_name = request.form.get('sight_name').title().strip() #sight they choose

    # sights added to database only once
    top_sights = Sight.query.filter_by(name_sight=sight_name).all()
    sights = []
    i = 0
    while i < len(top_sights):
        sights.append(top_sights[i].name_sight)
        i+=1
    if sight_name not in sights:
        sight = Sight(name_sight=sight_name, city=city)
        db.session.add(sight)
        db.session.commit()

    # get sight_id and trip_id to add to trip_sight table in database
    sight_query = Sight.query.filter_by(name_sight=sight_name, city=city).all()
    sight_id = sight_query[0].sight_id
    trip = request.form.get('trip').title().strip() #trip they choose
    trip_user= Trip.query.filter_by(trip_name=trip, user_id=user_id).all()
    trip_id= trip_user[0].trip_id

    #can only add trip_id and sight_id once in trip_sights table
    trip_sights_query = Trip_sight.query.filter_by(trip_id=trip_id, sight_id=sight_id).all()
    trip_sights = []

    j = 0
    while j < len(trip_sights_query):
        trip_sights.append(trip_sights_query[j].trip_id)
        trip_sights.append(trip_sights_query[j].sight_id)
        i+=1
    if trip_id not in trip_sights and sight_id not in trip_sights:
        trip_sight = Trip_sight(trip_id=trip_id, sight_id=sight_id)
        db.session.add(trip_sight)
        db.session.commit()

    return "Success"

@app.route('/delete_trip', methods=['POST'])
def delete_trips():
    """Delete trip folder"""
    user_id = session['user']
    trip_del = request.form.get('trip_del').strip()

    del_trip = Trip.query.filter_by(trip_name=trip_del, user_id=user_id).first()
    trip_id = del_trip.trip_id
    del_trip_sights = Trip_sight.query.filter_by(trip_id=trip_id).all()

    for sights in del_trip_sights:
        db.session.delete(sights)

    db.session.delete(del_trip)
    db.session.commit()

    return redirect('/trips')

# @app.route('/edit_trip', methods=['POST'])
# def edit_trips():
#     """Edit trip folder"""
#     user_id = session['user']
    # trip_edit = request.form.get('trip_edit').strip()
    # put in = request.form.get('trip_edit').strip()

    # edit_trip = Trip.query.filter_by(trip_name=trip_edit, user_id=user_id).first()
    # edit_trip.trip_name = put in

    # db.session.commit()

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