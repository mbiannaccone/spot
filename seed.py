"""Utility file to store data in database."""

from sqlalchemy import func
from model import (User, Breeder, BreederPhoto, Litter, LitterPhoto, Pup,
                   PupPhoto, Dog, DogPhoto, DogLitter, Gender, Award, Event,
                   EventPhoto, Blog, Breed)
from model import connect_to_db, db
from server import app
from datetime import datetime

def load_breeds():
    """Loads in breed information from akc website."""

    