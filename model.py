"""Models and database functions for project."""

from flask_sqlalchemy import SQLAlchemy
import correlation
from datetime import datetime

db = SQLAlchemy()

##############################################################################
# Model definitions


class Users(db.Model):
    """Users of the site."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    zipcode = db.Column(db.String(15), nullable=False)
    phone = db.Column(db.String(25))

    def __repr__(self):
        return '<User %s, email: %s>' % (self.user_id, self.email)


class Breeders(db.Model):
    """Breeders on the site."""

    __tablename__ = "breeders"

    # do i need to also designate as primary key?
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    bio = db.Column(db.String(5000))
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(25))
    email = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Breeder %s, name: %s>' % (self.user_id, self.name)


class BreederPhotos(db.Model):
    """Photos for the breeders homepage."""

    __tablename__ = "breeder_photos"

    photo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('breeders.user_id'))
    photo = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(500))

    def __repr__(self):
        return '<Photo %s, user_id: %s>' % (self.photo_id, self.user_id)


class BlogPosts(db.Model):
    """Blog posts from the breeder."""

    __tablename__ = "blog_posts"

    blog_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('breeders.user_id'))
    date = db.Column(db.DateTime)
    category = db.Column(db.String(25), nullable=False)
    post = db.Column(db.String(5000), nullable=False)

    def __repr__(self):
        return '<Blog Post %s, user_id: %s, category: %s' % (self.blog_id,
                                                             self.user_id,
                                                             self.category)


class Awards(db.Model):
    """Certifications/Awards the breeder has won."""

    __tablename__ = "awards"

    award_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('breeders.user_id'))
    dog_id = db.Column(db.Integer, db.ForeignKey('dogs.dog_id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(400))
    date = db.Column(db.DateTime)

    def __repr__(self):
        return '<Award %s, user_id: %s, dog_id: %s, name: %s>' % (self.award_id,
                                                                  self.user_id,
                                                                  self.dog_id,
                                                                  self.name)


class Litters(db.Model):
    """Litters of puppies from a breeder."""

    __tablename__ = "litters"

    litter_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('breeders.user_id'))
    breed = db.Column(db.String(100), nullable=False)
    date_born = db.Column(db.DateTime)
    date_available = db.Column(db.DateTime)
    description = db.Column(db.String(1000))
    dam_id = db.Column(db.Integer, db.ForeignKey('dogs.dog_id'))
    sire_id = db.Column(db.Integer, db.ForeignKey('dogs.dog_id'))
    num_pups = db.Column(db.Integer)

    def __repr__(self):
        return '<Litter %s, user_id: %s, breed: %s>' % (self.litter_id,
                                                        self.user_id,
                                                        self.breed)


class LitterPhotos(db.Model):
    """Photos of litters for a litter's homepage."""

    __tablename__ = "litter_photos"

    photo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    litter_id = db.Column(db.Integer, db.ForeignKey('litters.litter_id'))
    photo = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(500))

    def __repr__(self):
        return '<Litter Photo %s, litter_id: %s>' % (self.photo_id,
                                                     self.litter_id)


class Pups(db.Model):
    """Individual puppies from a litter."""

    __tablename__ = "pups"

    pup_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    litter_id = db.Column(db.Integer, db.ForeignKey('litters.litter_id'))
    name = db.Column(db.String(50))
    available = db.Column(db.String(1), default='y')  # once taken, update to n
    gender = db.Column(db.String(1), db.ForeignKey('genders.gender_id'))
    description = db.Column(db.String(1000))
    price = db.Column(db.Float)

    def __repr__(self):
        return '<Pup %s, name: %s, litter_id: %s>' % (self.pup_id,
                                                      self.name,
                                                      self.litter_id)


class PupPhotos(db.Model):
    """Photos of individual puppies."""

    __tablename__ = "pup_photos"

    photo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    pup_id = db.Column(db.Integer, db.ForeignKey('pups.pup_id'))
    photo = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(500))

    def __repr__(self):
        return '<Pup Photo %s, pup_id: %s>' % (self.photo_id, self.pup_id)


class Dogs(db.Model):
    """Individual dams and sires owned by the breeder."""

    __tablename__ = "dogs"

    dog_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50))
    litter_id = db.Column(db.Integer, db.ForeignKey('litters.litter_id'))
    date_born = db.Column(db.DateTime)
    gender = db.Column(db.String(1), db.ForeignKey('genders.gender_id'))
    description = db.Column(db.String(1000))

    def __repr__(self):
        return '<Dog %s, name: %s, gender: %s>' % (self.dog_id,
                                                   self.name,
                                                   self.gender)


class DogPhotos(db.Model):
    """Photos of individual dogs."""

    __tablename__ = "dog_photos"

    photo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('dogs.dog_id'))
    photo = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(500))

    def __repr__(self):
        return '<Dog Photo %s, dog_id: %s>' % (self.photo_id, self.dog_id)


class Genders(db.Model):
    """Genders (male or female) for pups and dogs."""

    __tablename__ = "genders"

    gender_id = db.Column(db.String(1), primary_key=True)
    gender = db.Column(db.String(6), nullable=False)

    def __repr__(self):
        return '<Gender %s, %s>' % (self.gender_id, self.gender)


class Events(db.Model):
    """Breeder events."""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('breeders.user_id'))
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    date = db.Column(db.DateTime)

    def __repr__(self):
        return '<Event %s, user_id: %s, name: %s>' % (self.event_id,
                                                      self.user_id,
                                                      self.name)


class EventPhotos(db.Model):
    """Photos from breeder events."""

    __tablename__ = "event_photos"

    photo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    event_id = db.Coumn(db.Integer, db.ForeignKey('events.event_id'))
    photo = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(500))

    def __repr__(self):
        return '<Event Photo %s, event_id: %s>' % (self.photo_id, self.event_id)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///dogs'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."
