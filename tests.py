""" Tests for server.py. """

from unittest import TestCase
from model import connect_to_db, db, example_data
from server import app
from flask import session


# class FlaskTestsBasic(TestCase):
#     """ Flask tests for testing Spot's server. """

#     def setUp(self):
#         self.client = app.test_client()
#         app.config['TESTING'] = True

#     def test_login(self):
#         """ Tests login - assuming not logged in yet. """
#         result = self.client.get('/login')
#         self.assertIn('Please enter your email and password', result.data)

#     def test_register(self):
#         """ Tests register - assuming not logged in yet. """
#         result = self.client.get('/register')
#         self.assertIn('Please enter your information below', result.data)


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
        self.assertIn('welcome', result.data)
        self.assertIn('Sporting Group', result.data)

    # def test_breed_search(self):
    #     """ Tests breed search results page. """
    #     result = self.client.get('/breed-search')
    #     self.assertIn('Results', result.data)

    # def test_breeder_search(self):
    #     """ Tests breeder search results page. """
    #     result = self.client.get('/breeder-search')
    #     self.assertIn('breeder results near', result.data)

if __name__ == "__main__":
    import unittest
    unittest.main()
