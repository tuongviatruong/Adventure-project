import unittest

from server import app
from flask import session
from model import db, connect_to_db, example_data

class Tests(unittest.TestCase):
    """Tests for my adventure site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("Search a city for top sights", result.data)

    def test_login_form(self):
        result = self.client.get("/login-form")
        self.assertIn("Email:", result.data)
        self.assertIn("Password:", result.data)

    def test_register_form(self):
        result = self.client.get("/register-form")
        self.assertIn("Registration", result.data)
        self.assertIn("First name: ", result.data)


class TestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        app.config['SECRET_KEY'] = 'key'

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user'] = 1

    # def tearDown(self):
    #     """Do at end of every test."""

    #     db.session.close()
    #     db.drop_all()

    def test_login(self):
        result = self.client.post("/login",
                                    data={'email': 'vi@gmail.com', 'password':'hello'},
                                    follow_redirects=True)
        self.assertIn("Your Trips:", result.data)
        self.assertIn("Log Out", result.data)

    def test_trips(self):
        """Test trips page."""

        result = self.client.get("/trips")
        self.assertIn("Chicago 2018", result.data)
        self.assertIn("New York 2019", result.data)

    def test_trips_details(self):
        """Test trips page."""

        result = self.client.get("/details/Chicago%202018")
        self.assertIn("The Cloud Gate", result.data)
        result = self.client.get("/details/New%20York%202019")
        self.assertIn("Brooklyn Bridge", result.data)


if __name__ == "__main__":
    unittest.main()