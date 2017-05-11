"""Utility file to store data in database."""

from sqlalchemy import func
from model import (Award, Blog, Breed, BreedChar, Breeder, BreederPhoto, Char,
                   Dog, DogPhoto, Energy, Event, EventPhoto, Gender, Group,
                   Litter, LitterPhoto, Pup, PupPhoto, Size, User)
from model import connect_to_db, db
from server import app
from datetime import datetime, timedelta
from random import randint


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


def load_breeders():
    """ Loads in breeders from breeder_data.txt. """

    print "Breeders"

    counter = 0

    for row in open("seed_data/breeder_data.txt"):
        row = row.rstrip().split('\t')
        bio, name, addy, ph, em = row
        counter += 1

        breeder = Breeder(bio=bio, name=name, address=addy, phone=ph[-13:],
                          email=em, user_id=counter)

        db.session.add(breeder)

    db.session.commit()


def load_breeds():
    """ Loads in breeds from breed_data.txt. """

    print "Breeds"

    for row in open("seed_data/breed_data.txt"):
        row = row.rstrip().split('\t')
        name, descr, group, size, energy, url, pic = row
        group_dict = {'Sporting Group': 1, 'Herding Group': 2, 'Hound Group': 3,
                      'Non-Sporting Group': 4, 'Terrier Group': 5, 'Toy Group': 6,
                      'Working Group': 7, 'Foundation Stock Service': 8}
        group_id = group_dict[group]

        breed = Breed(name=name, akc_url=url, group_id=group_id, size_id=size,
                      energy_id=energy, description=descr, photo=pic)
        db.session.add(breed)

    db.session.commit()


def load_litters():
    """ Loads in litters from litter_data.txt. """

    print "Litters"

    for row in open("seed_data/litter_data.txt"):
        row = row.rstrip().split('\t')
        date_born = datetime.strptime(row[0], "%m/%d/%Y")
        date_available = date_born + timedelta(days=56)
        num_pups = row[3]
        descr = 'so cute'
        user_id = randint(1, 560)
        breed_id = randint(1, 256)
        sire_id = randint(501, 1000)
        dam_id = randint(1, 500)

        litter = Litter(user_id=user_id, breed_id=breed_id, date_born=date_born,
                        date_available=date_available, description=descr,
                        num_pups=num_pups, sire_id=sire_id, dam_id=dam_id)

        db.session.add(litter)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Seed the tables with data
    load_genders()
    load_energies()
    load_chars()
    load_sizes()
    load_groups()
    load_users()
    load_breeders()
    load_breeds()
    # load_litters()    
