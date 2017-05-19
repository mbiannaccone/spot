"""Models and database functions for project."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

##############################################################################
# Model definitions


class User(db.Model):
    """A user of the site."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
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

    breeder_id = db.Column(db.Integer,
                           db.ForeignKey('users.user_id'),
                           primary_key=True)
    bio = db.Column(db.String(5000))
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(25))
    email = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Breeder %s, name: %s>' % (self.breeder_id, self.name)


class BreederPhoto(db.Model):
    """A photo for the breeder's homepage."""

    __tablename__ = "breeder_photos"

    photo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    breeder_id = db.Column(db.Integer, db.ForeignKey('breeders.breeder_id'))
    photo = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(500))

    breeder = db.relationship('Breeder', backref='photos')

    def __repr__(self):
        return '<Photo %s, breeder_id: %s>' % (self.photo_id, self.breeder_id)


class Blog(db.Model):
    """A blog post from the breeder."""

    __tablename__ = "blog_posts"

    blog_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    breeder_id = db.Column(db.Integer, db.ForeignKey('breeders.breeder_id'))
    date = db.Column(db.DateTime)
    category = db.Column(db.String(25), nullable=False)
    post = db.Column(db.String(5000), nullable=False)

    breeder = db.relationship('Breeder', backref='blogs')

    def __repr__(self):
        return '<Blog Post %s, breeder_id: %s, category: %s' % (self.blog_id,
                                                                self.breeder_id,
                                                                self.category)


class Award(db.Model):
    """A certification/award that the breeder has won."""

    __tablename__ = "awards"

    award_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    breeder_id = db.Column(db.Integer, db.ForeignKey('breeders.breeder_id'))
    dog_id = db.Column(db.Integer, db.ForeignKey('dogs.dog_id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(400))
    date = db.Column(db.DateTime)

    breeder = db.relationship('Breeder', backref='awards')
    dog = db.relationship('Dog', backref='awards')

    def __repr__(self):
        return '<Award %s, breeder_id: %s, dog_id: %s, name: %s>' % (self.award_id,
                                                                     self.breeder_id,
                                                                     self.dog_id,
                                                                     self.name)


class Litter(db.Model):
    """A litter of puppies from a breeder."""

    __tablename__ = "litters"

    litter_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    breeder_id = db.Column(db.Integer, db.ForeignKey('breeders.breeder_id'))
    breed_id = db.Column(db.Integer, db.ForeignKey('breeds.breed_id'))
    date_born = db.Column(db.DateTime)
    date_available = db.Column(db.DateTime)
    description = db.Column(db.String(1000))
    num_pups = db.Column(db.Integer)
    sire_id = db.Column(db.Integer, db.ForeignKey('dogs.dog_id'))
    dam_id = db.Column(db.Integer, db.ForeignKey('dogs.dog_id'))

    sire = db.relationship('Dog', foreign_keys=[sire_id])
    dam = db.relationship('Dog', foreign_keys=[dam_id])
    breeder = db.relationship('Breeder', backref='litters')
    breed = db.relationship('Breed', backref='litters')

    def __repr__(self):
        return '<Litter %s, breeder_id: %s, breed: %s>' % (self.litter_id,
                                                           self.breeder_id,
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
    available = db.Column(db.Boolean, default=True)
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
    breeder_id = db.Column(db.Integer, db.ForeignKey('breeders.breeder_id'))
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    date = db.Column(db.DateTime)

    breeder = db.relationship('Breeder', backref='events')

    def __repr__(self):
        return '<Event %s, breeder_id: %s, name: %s>' % (self.event_id,
                                                         self.breeder_id,
                                                         self.name)


class EventPhoto(db.Model):
    """A photo from a breeder event."""

    __tablename__ = "event_photos"

    photo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))
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
    size_id = db.Column(db.String(1), db.ForeignKey('sizes.size_id'))
    energy_id = db.Column(db.String(1), db.ForeignKey('energies.energy_id'))
    description = db.Column(db.String(500))
    photo = db.Column(db.String(150))

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

    size_id = db.Column(db.String(1), primary_key=True)
    size = db.Column(db.String(6), nullable=False)

    def __repr__(self):
        return '<Size %s>' % (self.size)


class Energy(db.Model):
    """A breed energy level."""

    __tablename__ = "energies"

    energy_id = db.Column(db.String(1), primary_key=True)
    energy = db.Column(db.String(6), nullable=False)

    def __repr__(self):
        return '<Energy %s>' % (self.energy)


class BreedChar(db.Model):
    """A breed's characteristic."""

    __tablename__ = "breed_chars"

    breedchar_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    breed_id = db.Column(db.Integer, db.ForeignKey('breeds.breed_id'))
    char_id = db.Column(db.Integer, db.ForeignKey('chars.char_id'))
    description = db.Column(db.String(5000))

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


class BreederSpot(db.Model):
    """A breeder that a user has spotted ('liked')."""

    __tablename__ = "breeder_spots"

    spot_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    breeder_id = db.Column(db.Integer, db.ForeignKey('breeders.breeder_id'))

    user = db.relationship('User', backref='breeder_spots')
    breeder = db.relationship('Breeder', backref='breeder_spots')

    def __repr__(self):
        return '<User %s, Breeder %s>' % (self.user_id, self.breeder_id)


class BreedSpot(db.Model):
    """A breed that a user has spotted ('liked')."""

    __tablename__ = "breed_spots"

    spot_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    breed_id = db.Column(db.Integer, db.ForeignKey('breeds.breed_id'))

    user = db.relationship('User', backref='breed_spots')
    breed = db.relationship('Breed', backref='breed_spots')

    def __repr__(self):
        return '<User %s, Breed %s>' % (self.user_id, self.breed_id)

##############################################################################
# Helper functions


def connect_to_db(app, db_uri='postgresql:///dogs'):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    db.app = app
    db.init_app(app)


def example_data():
    """Create some sample data for testing."""

    # empty out existing data (in case run more than once)
    for class_name in [User,
                       Breeder,
                       BreederPhoto,
                       Event,
                       EventPhoto,
                       Litter,
                       LitterPhoto,
                       Blog,
                       Group,
                       Size,
                       Energy,
                       Breed,
                       Char,
                       BreedChar,
                       Dog,
                       DogPhoto,
                       Pup,
                       PupPhoto,
                       Gender,
                       Award,
                       BreederSpot,
                       BreedSpot]:
        class_name.query.delete()

    # add sample data to each table
    gender1 = Gender(gender_id='m', gender="male")
    gender2 = Gender(gender_id='f', gender="female")
    group = Group(group_id=1, name="Sporting Group", description="We hunt.")
    size = Size(size_id='m', size="Medium")
    energy = Energy(energy_id='h', energy="High")
    breed = Breed(breed_id=1,
                  name="German Shorthaired Pointer",
                  akc_url="http://www.akc.org/dog-breeds/german-shorthaired-pointer/",
                  group_id=1,
                  size_id='m',
                  energy_id='h',
                  photo='http://cdn.akc.org/akcdoglovers/German-Shorthaired-Pointer_163X140.jpg',
                  description='Friendly, smart, willing to please.')
    user1 = User(user_id=1,
                 email="breeder@gmail.com",
                 password="pwd",
                 fname="Bob",
                 lname="Smith",
                 zipcode="94123",
                 phone="(415)441-4441")
    user2 = User(user_id=2,
                 email="normaluser@gmail.com",
                 password="pword",
                 fname="Shelly",
                 lname="Dog-Lover",
                 zipcode="94123",
                 phone="(415)551-5151")
    breeder = Breeder(breeder_id=1,
                      bio="Hi, I'm a breeder",
                      name="Dog Breeder & Co.",
                      address="4101 Las Posas Rd, Camarillo, CA 93010",
                      phone="(415)555-5551",
                      email="dogs@breeder.com")
    breederphoto = BreederPhoto(breeder_id=1,
                                photo="http://www.tucsonadventuredogranch.com/morning_ruckus_at_Tucson_Adventure__Dog_Ranch.JPG",
                                caption="This is my ranch.")
    litter = Litter(litter_id=1,
                    breeder_id=1,
                    breed_id=1,
                    date_born=datetime.strptime("3/1/2017", "%m/%d/%Y"),
                    date_available=datetime.strptime("4/15/2017", "%m/%d/%Y"),
                    description="We had some cute puppies!",
                    num_pups=4,
                    sire_id=1,
                    dam_id=1)
    litterphoto = LitterPhoto(litter_id=1,
                              photo="http://www.cutestpaw.com/wp-content/uploads/2011/11/Puppies.jpg",
                              caption="Look at these cute puppies!")
    event = Event(event_id=1,
                  breeder_id=1,
                  name="Doggy Day Care",
                  description="Bring your dogs for a fun day of playtime!",
                  date=datetime.strptime("6/1/2017", "%m/%d/%Y"))
    eventphoto = EventPhoto(event_id=1,
                            photo="http://815678169699-bfas-files.s3.amazonaws.com/s3fs-public/pages/Strut-Your-Mutt-dog-walk-fundraiser-152.jpg",
                            caption="Look at us having fun!")
    blog = Blog(breeder_id=1,
                date=datetime.strptime("3/15/2017", "%m/%d/%Y"),
                category="Puppies",
                post="The puppies were born 2 weeks ago. They're getting so big!")
    char = Char(char_id=1, char='Health')
    breedchar = BreedChar(breed_id=1,
                          description="GSP's are generally healthy",
                          char_id=1)
    dog1 = Dog(dog_id=1,
               name="George",
               date_born=datetime.strptime("4/15/2015", "%m/%d/%Y"),
               gender_id='m',
               description='George is the best!')
    dog2 = Dog(dog_id=2,
               name="Georgina",
               date_born=datetime.strptime("8/15/2015", "%m/%d/%Y"),
               gender_id='f',
               description="Georgina is a beautiful dam.")
    dogphoto1 = DogPhoto(dog_id=1,
                         photo="https://upload.wikimedia.org/wikipedia/commons/3/38/Duitse_staande_korthaar_10-10-2.jpg",
                         caption="Look it's George")

    dogphoto2 = DogPhoto(dog_id=2,
                         photo="https://www.gundogbreeders.com/images/pedigrees/1134.jpg",
                         caption="Look it's Georgina!")
    pup = Pup(litter_id=1,
              name="Lila",
              available=True,
              gender_id='f',
              description="perfect little puppy",
              price=5000)
    pupphoto = PupPhoto(pup_id=1,
                        photo="http://imglf2.ph.126.net/8Cv0GXgUprkT3RLckqTOOg==/6619212831327919772.jpg",
                        caption="Look I'm a cute puppy")
    award1 = Award(breeder_id=1,
                   dog_id=1,
                   name="Cutest Dog in Town",
                   description="Crowned to the cutest dog in town.",
                   date=datetime.strptime("8/15/2016", "%m/%d/%Y"))
    award2 = Award(breeder_id=1,
                   dog_id=2,
                   name="Prettiest Dog in Town",
                   description="Crowned to the prettiest dog in town.",
                   date=datetime.strptime("12/15/2016", "%m/%d/%Y"))
    breederspot = BreederSpot(user_id=2,
                              breeder_id=1)
    breedspot = BreedSpot(user_id=2,
                          breed_id=1)

    db.session.add_all([gender1,
                        gender2,
                        group,
                        size,
                        energy,
                        breed,
                        user1,
                        user2,
                        breeder,
                        breederphoto,
                        litter,
                        litterphoto,
                        event,
                        eventphoto,
                        blog,
                        char,
                        breedchar,
                        dog1,
                        dog2,
                        dogphoto1,
                        dogphoto2,
                        pup,
                        pupphoto,
                        award1,
                        award2,
                        breederspot,
                        breedspot])
    db.session.commit()


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    db.create_all()
    example_data()
    print "Connected to DB."
