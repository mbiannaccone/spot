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

    print 'Genders'

    female = Gender(gender_id='f', gender='Female')
    male = Gender(gender_id='m', gender='Male')

    db.session.add_all([male, female])
    db.session.commit()


def load_energies():
    """ Loads in energy possibilities. """

    print 'Energies'

    low = Energy(energy_id='l', energy='Low')
    med = Energy(energy_id='m', energy='Medium')
    high = Energy(energy_id='h', energy='High')

    db.session.add_all([low, med, high])
    db.session.commit()


def load_sizes():
    """ Loads in size possibilities. """

    print "Sizes"

    small = Size(size_id='s', size='Small')
    med = Size(size_id='m', size='Medium')
    large = Size(size_id='l', size='Large')

    db.session.add_all([small, med, large])

    db.session.commit()


def load_chars():
    """ Loads in characteristic possibilities from char_data file. """

    print "Chars"

    for row in open("seed_data/char_data.txt"):
        row = row.rstrip()
        new_char = Char(char=row)
        db.session.add(new_char)

    db.session.commit()


def load_groups():
    """ Loads in group possibilities. """

    print "Groups"

    for row in open("seed_data/group_data.txt"):
        row = row.rstrip().split('|')
        name, description = row
        group = Group(name=name, description=description)
        db.session.add(group)

    db.session.commit()


def load_users():
    """ Loads in users from user_data.txt. """

    print "Users"

    for row in open("seed_data/user_data.txt"):
        row = row.rstrip().split('\t')
        auto, first, last, email, pwd, zipc, ph = row
        user = User(email=email, password=pwd, fname=first, lname=last,
                    zipcode=zipc, phone=ph[-13:])
        db.session.add(user)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Seed the tables with data
    # load_genders()
    # load_energies()
    # load_chars()
    # load_sizes()
    # load_groups()
    load_users()
