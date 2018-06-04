"""Models and database functions for Adventure planning project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Model definitions

class User(db.Model):
    """User of website"""
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(64))
    lname = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password = db.Column(db.String(64))

    def __repr__(self):
        """Provide helpful representation when printed"""
        return "<User user_id={} fname={} lname={}>".format(self.user_id,
                                                        self.fname, self.lname)

class Sight(db.Model):
    """Top sights saved in user's Trip folder"""
    __tablename__ = "sights"

    sight_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name_sight = db.Column(db.String(64))
    city = db.Column(db.String(64))
    category = db.Column(db.String(64))

    def __repr__(self):
        """Provide helpful representation when printed"""
        return "<Sight sight_id={} name={} city={} >".format(self.sight_id, self.name_sight, self.city)

class Trip(db.Model):
    """Folder of trips for each user with city name and sights of each city"""
    __tablename__ = "trips"

    trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trip_name = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    #Define relationship to user
    user = db.relationship("User", backref="trips")

    def __repr__(self):
        """Provide helpful representation when printed"""
        return "<Trip trip_id={} trip_name={}>".format(self.trip_id, self.trip_name)

class Trip_sight(db.Model):
    """Association table for Sight and Trip tables"""
    __tablename__ = "trip_sights"

    trip_sight_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.trip_id'))
    sight_id = db.Column(db.Integer, db.ForeignKey('sights.sight_id'))

    #Define relationship to trip
    trip = db.relationship("Trip", backref="trip_sights")
    #Define relationship to sight
    sight = db.relationship("Sight", backref="trip_sights")

    def __repr__(self):
        """Provide helpful representation when printed"""
        return "<Trip_sight trip_sight_id={} trip_id={} sight_id={}>".format(
                                                            self.trip_sight_id,
                                                    self.trip_id, self.sight_id)

class Todo_list(db.Model):
    """Association table for User and Trip tables for todo list"""
    __tablename__ = "todo_lists"

    todo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.trip_id'))
    todo = db.Column(db.UnicodeText)

    #Define relationship to trip
    trips = db.relationship("Trip", backref="todo_lists")
    #Define relationship to user
    users = db.relationship("User", backref="todo_lists")

    def __repr__(self):
        """Provide helpful representation when printed"""
        return "<Todo todo_id={} trip_id={} todo={}>".format(
                                                    self.todo_id,
                                                    self.trip_id, self.todo)    

def example_data():
    user = User(fname="Vi", lname="truong", email="vi@gmail.com", password="hello")

    trip1 = Trip(trip_name="Chicago 2018", user=user)
    trip2 = Trip(trip_name="New York 2019", user=user)

    sight1 = Sight(name_sight="The Cloud Gate", city="Chicago")
    sight2 = Sight(name_sight="Brooklyn Bridge", city="New york")

    trip_sight1 = Trip_sight(trip=trip1, sight=sight1)
    trip_sight2 = Trip_sight(trip=trip2, sight=sight2)

    todo1 = Todo_list(users=user, trips=trip1, todo="Need to book ticket for Cloud Gate")

    db.session.add_all([user, trip1, trip2, sight1,
                        sight2, trip_sight1, trip_sight2, todo1])
    db.session.commit()


##############################################################################
# Helper functions

def connect_to_db(app, db_uri="postgresql:///trips"):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."