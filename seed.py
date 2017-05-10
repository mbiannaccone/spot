"""Utility file to store data in database."""

from sqlalchemy import func
from model import (Award, Blog, Breed, BreedChar, Breeder, BreederPhoto, Char,
                   Dog, DogPhoto, Energy, Event, EventPhoto, Gender, Group,
                   Litter, LitterPhoto, Pup, PupPhoto, Size, User)
from model import connect_to_db, db
from server import app
from datetime import datetime


def load_genders():
    """ Loads in gender possibilities. """

    print 'genders'

    female = Gender('f', 'female')
    male = Gender('m', 'male')

    db.session.add_all([male, female])
    db.session.commit()


def load_energies():
    """ Loads in energy possibilities. """

    print 'energies'

    low = Energy('l', 'low')
    med = Energy('m', 'medium')
    high = Energy('h', 'high')

    db.session.add_all([low, med, high])
    db.session.commit()


def load_char():
    """ Loads in characteristic possibilities from char_data file. """


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()
