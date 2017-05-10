"""Models and database functions for project."""

from flask_sqlalchemy import SQLAlchemy
import correlation

db = SQLAlchemy()

##############################################################################
# Model definitions


class User(db.Model):
    """A user of the site."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    zipcode = db.Column(db.String(15), nullable=False)
    phone = db.Column(db.String(25))

    breeder = db.relationship('Breeder', uselist=False, backref='user')

    def __repr__(self):
        return '<User %s, email: %s>' % (self.user_id, self.email)


class Breeder(db.Model):
    """A breeder on the site."""

    __tablename__ = "breeders"

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        primary_key=True)
    bio = db.Column(db.String(5000))
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(25))
    email = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Breeder %s, name: %s>' % (self.user_id, self.name)


class BreederPhoto(db.Model):
    """A photo for the breeder's homepage."""

    __tablename__ = "breeder_photos"

    photo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('breeders.user_id'))
    photo = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(500))

    breeder = db.relationship('Breeder', backref='photos')

    def __repr__(self):
        return '<Photo %s, user_id: %s>' % (self.photo_id, self.user_id)


class Blog(db.Model):
    """A blog post from the breeder."""

    __tablename__ = "blog_posts"

    blog_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('breeders.user_id'))
    date = db.Column(db.DateTime)
    category = db.Column(db.String(25), nullable=False)
    post = db.Column(db.String(5000), nullable=False)

    breeder = db.relationship('Breeder', backref='blogs')

    def __repr__(self):
        return '<Blog Post %s, user_id: %s, category: %s' % (self.blog_id,
                                                             self.user_id,
                                                             self.category)


class Award(db.Model):
    """A certification/award that the breeder has won."""

    __tablename__ = "awards"

    award_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('breeders.user_id'))
    dog_id = db.Column(db.Integer, db.ForeignKey('dogs.dog_id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(400))
    date = db.Column(db.DateTime)

    breeder = db.relationship('Breeder', backref='awards')
    dog = db.relationship('Dog', backref='awards')

    def __repr__(self):
        return '<Award %s, user_id: %s, dog_id: %s, name: %s>' % (self.award_id,
                                                                  self.user_id,
                                                                  self.dog_id,
                                                                  self.name)


class Litter(db.Model):
    """A litter of puppies from a breeder."""

    __tablename__ = "litters"

    litter_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('breeders.user_id'))
    breed_id = db.Column(db.Integer, db.ForeignKey('breeds.breed_id'))
    date_born = db.Column(db.DateTime)
    date_available = db.Column(db.DateTime)
    description = db.Column(db.String(1000))
    num_pups = db.Column(db.Integer)
    sire_id = db.Columnm(db.Integer, db.ForeignKey('dogs.dog_id'))
    dam_id = db.Columnm(db.Integer, db.ForeignKey('dogs.dog_id'))

    dog = db.relationship('Dog', backref='litters')
    breeder = db.relationship('Breeder', backref='litters')
    breed = db.relationship('Breed', backref='litters')

    def __repr__(self):
        return '<Litter %s, user_id: %s, breed: %s>' % (self.litter_id,
                                                        self.user_id,
                                                        self.breed)


class LitterPhoto(db.Model):
    """A photo of a litter."""

    __tablename__ = "litter_photos"

    photo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    litter_id = db.Column(db.Integer, db.ForeignKey('litters.litter_id'))
    photo = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(500))

    litter = db.relationship('Litter', backref='photos')

    def __repr__(self):
        return '<Litter Photo %s, litter_id: %s>' % (self.photo_id,
                                                     self.litter_id)


class Pup(db.Model):
    """A puppy from a litter."""

    __tablename__ = "pups"

    pup_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    litter_id = db.Column(db.Integer, db.ForeignKey('litters.litter_id'))
    name = db.Column(db.String(50))
    available = db.Column(db.String(1), default='y')  # once taken, update to n
    gender_id = db.Column(db.String(1), db.ForeignKey('genders.gender_id'))
    description = db.Column(db.String(1000))
    price = db.Column(db.Float)

    litter = db.relationship('Litter', backref='pups')
    gender = db.relationship('Gender', backref='pups')

    def __repr__(self):
        return '<Pup %s, name: %s, litter_id: %s>' % (self.pup_id,
                                                      self.name,
                                                      self.litter_id)


class PupPhoto(db.Model):
    """A photo of a puppy."""

    __tablename__ = "pup_photos"

    photo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    pup_id = db.Column(db.Integer, db.ForeignKey('pups.pup_id'))
    photo = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(500))

    pup = db.relationship('Pup', backref='photos')

    def __repr__(self):
        return '<Pup Photo %s, pup_id: %s>' % (self.photo_id, self.pup_id)


class Dog(db.Model):
    """A dam or sire owned by the breeder."""

    __tablename__ = "dogs"

    dog_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50))
    date_born = db.Column(db.DateTime)
    gender_id = db.Column(db.String(1), db.ForeignKey('genders.gender_id'))
    description = db.Column(db.String(1000))

    gender = db.relationship('Gender', backref='dogs')

    def __repr__(self):
        return '<Dog %s, name: %s, gender: %s>' % (self.dog_id,
                                                   self.name,
                                                   self.gender)


class DogPhoto(db.Model):
    """A phogo of a dog(dam or sire)."""

    __tablename__ = "dog_photos"

    photo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('dogs.dog_id'))
    photo = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(500))

    dog = db.relationship('Dog', backref='photos')

    def __repr__(self):
        return '<Dog Photo %s, dog_id: %s>' % (self.photo_id, self.dog_id)


class Gender(db.Model):
    """A gender (male or female) for pups and dogs."""

    __tablename__ = "genders"

    gender_id = db.Column(db.String(1), primary_key=True)
    gender = db.Column(db.String(6), nullable=False)

    def __repr__(self):
        return '<Gender %s, %s>' % (self.gender_id, self.gender)


class Event(db.Model):
    """A breeder events."""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('breeders.user_id'))
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    date = db.Column(db.DateTime)

    breeder = db.relationship('Breeder', backref='events')

    def __repr__(self):
        return '<Event %s, user_id: %s, name: %s>' % (self.event_id,
                                                      self.user_id,
                                                      self.name)


class EventPhoto(db.Model):
    """A photo from a breeder event."""

    __tablename__ = "event_photos"

    photo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    event_id = db.Coumn(db.Integer, db.ForeignKey('events.event_id'))
    photo = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(500))

    event = db.relationship('Event', backref='photos')

    def __repr__(self):
        return '<Event Photo %s, event_id: %s>' % (self.photo_id, self.event_id)


class Breed(db.Model):
    """A dog breed."""

    __tablename__ = "breeds"

    breed_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    akc_url = db.Column(db.String(100))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'))
    size_id = db.Column(db.Integer, db.ForeignKey('sizes.size_id'))
    energy_id = db.Column(db.Integer, db.ForeignKey('energies.energy_id'))
    description = db.Column(db.String(500))

    group = db.relationship('Group', backref='breeds')
    size = db.relationship('Size', backref='breeds')
    energy = db.relationship('Energy', backref='breeds')

    def __repr__(self):
        return '<Breed %s, name: %s>' % (self.breed_id, self.name)


class Group(db.Model):
    """A breed group."""

    __tablename__ = "groups"

    group_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(2000))

    def __repr__(self):
        return '<Group %s, name: %s>' % (self.group_id, self.name)


class Size(db.Model):
    """A breed size."""

    __tablename__ = "sizes"

    size_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    size = db.Column(db.String(6), nullable=False)

    def __repr__(self):
        return '<Size %s>' % (self.size)


class Energy(db.Model):
    """A breed energy level."""

    __tablename__ = "energies"

    energy_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    energy = db.Column(db.String(6), nullable=False)

    def __repr__(self):
        return '<Energy %s>' % (self.energy)


class BreedChar(db.Model):
    """A breed's characteristic."""

    __tablename__ = "breed_chars"

    breedchar_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    breed_id = db.Column(db.Integer, db.ForeignKey('breeds.breed_id'))
    char_id = db.Column(db.Integer, db.ForeignKey('chars.char_id'))

    breed = db.relationship('Breed', backref='breed_chars')
    char = db.relationship('Char', backref='breed_chars')

    def __repr__(self):
        return '<Breed_id: %s, Char_id: %s>' % (self.breed_id, self.char_id)


class Char(db.Model):
    """A characteristic."""

    __tablename__ = "chars"

    char_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    char = db.Column(db.String(100))

    def __repr__(self):
        return '<Char: %s>' % (self.char)


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
