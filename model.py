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
    latitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)

    def __repr__(self):
        """Provide helpful representation when printed"""
        return "<Sight sight_id={} name={} city={} >".format(self.sight_id, 
                                                    self.name_sight, self.city)

class Trip(db.Model):
    """Folder of trips for each user with city name and sights of each city"""
    __tablename__ = "trips"

    trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    city = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    #Define relationship to user
    user = db.relationship("User", backref=db.backref("trips"))

    def __repr__(self):
        """Provide helpful representation when printed"""
        return "<Trip trip_id={} city={}>".format(self.trip_id, self.city)

class Trip_sight(db.Model):
    """Association table for Sight and Trip tables"""
    __tablename__ = "trip_sights"

    trip_sight_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.trip_id'))
    sight_id = db.Column(db.Integer, db.ForeignKey('sights.sight_id'))

    #Define relationship to trip
    trip = db.relationship("Trip", backref=db.backref("trip_sights"))
    #Define relationship to sight
    sight = db.relationship("Sight", backref=db.backref("trip_sights"))

    def __repr__(self):
        """Provide helpful representation when printed"""
        return "<Trip_sight trip_sight_id={} trip_id={} sight_id>".format(
                                                            self.trip_sight_id,
                                                    self.trip_id, self.sight_id)

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///trip_sights'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."