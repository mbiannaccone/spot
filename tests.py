""" Tests for server.py. """

from unittest import TestCase
from model import connect_to_db, db, example_data
from server import app
from flask import session


class FlaskTestsBasic(TestCase):
    """ Flask tests for testing Spot's server. """

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_login(self):
        """ Tests login - assuming not logged in yet. """
        result = self.client.get('/login')
        self.assertIn('please enter your email and password', result.data)

    def test_register(self):
        """ Tests register - assuming not logged in yet. """
        result = self.client.get('/register')
        self.assertIn('please enter your information below', result.data)


class FlaskTestsDatabase(TestCase):
    """ Flask tests for testing Spot's database. """

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_homepage(self):
        """ Tests home page. """
        result = self.client.get('/')
        self.assertIn('find a breed', result.data)
        self.assertIn('sporting group', result.data)
        self.assertIn('German Shorthaired Pointer', result.data)

    def test_breed_search(self):
        """ Tests breed search results page. """
        result = self.client.get('/breed-search')
        self.assertIn('find a breed - results', result.data)

    def test_breed_info(self):
        """ Tests breed info page. """
        result = self.client.get('/breeds/1')
        self.assertIn('Friendly, smart, willing to please', result.data)

    def test_breeder_search(self):
        """ Tests breeder search results page. """
        data = {'breed': '1', 'location': '94904'}
        result = self.client.get('/breeder-search', query_string=data, follow_redirects=True)
        self.assertIn('breeder results near', result.data)

    def test_breeder_info(self):
        """ Tests breeder info page. """
        result = self.client.get('/breeders/1')
        self.assertIn('Dog Breeder', result.data)

    def test_litter_info(self):
        """ Tests a breeder's litter info page. """
        result = self.client.get('/breeders/1/litters/1')
        self.assertIn('We had some cute puppies!', result.data)

    def test_dog_info(self):
        """ Tests a breeder's dog info page. """
        result = self.client.get('/breeders/1/dogs/1')
        self.assertIn('George is the best!', result.data)


class FlaskTestsLoggedOut(TestCase):
    """ Flask tests with user logged out of session. """

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_breeder_spot(self):
        """ Tests that a breeder spot will redirect to login - assuming not logged in. """
        result = self.client.post('/breeder-spot', follow_redirects=True)
        self.assertIn('please enter your email and password', result.data)

    def test_breed_spot(self):
        """ Tests that a breed spot will redirect to login - assuming not logged in. """
        result = self.client.post('/breed-spot', follow_redirects=True)
        self.assertIn('please enter your email and password', result.data)

    def test_user_info(self):
        """ Tests that a user's page will redirect to login - assuming not logged in. """
        result = self.client.get('/users/1', follow_redirects=True)
        self.assertIn('please enter your email and password', result.data)


class FlaskTestsLoggedIn(TestCase):
    """ Flask tests with user logged in to session. """

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_register(self):
        """ Tests that doesn't let you try register if already logged in. """
        result = self.client.get('/register', follow_redirects=True)
        self.assertIn('your breeder spots', result.data)

    def test_login(self):
        """ Tests that doesn't let you log in if already logged in. """
        result = self.client.get('/login', follow_redirects=True)
        self.assertIn('your breeder spots', result.data)

    def test_breeder_spot(self):
        """ Tests that a breeder spot will work - assuming logged in. """
        result = self.client.post('/breeder-spot', data={'breeder': '1'}, follow_redirects=True)
        self.assertIn('spotted this breeder: Dog Breeder', result.data)

    def test_breed_spot(self):
        """ Tests that a breed spot will work - assuming logged in. """
        result = self.client.post('/breed-spot', data={'breed': '1'}, follow_redirects=True)
        self.assertIn('spotted the German Shorthaired Pointer breed!', result.data)

if __name__ == "__main__":
    import unittest
    unittest.main()
