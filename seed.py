"""Utility file to store data in database."""

from model import (Award, Blog, Breed, BreedChar, Breeder, BreederPhoto, PupPhoto,
                   Dog, DogPhoto, Energy, Event, EventPhoto, Gender, Group, Pup,
                   Litter, LitterPhoto, Char, Size, User, BreedSpot, BreederSpot)
from model import connect_to_db, db
from server import app
from datetime import datetime, timedelta
from random import choice, randint


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

        user = User(email='e'+email, password=pwd, fname=first, lname=last,
                    zipcode=zipc, phone=ph[-13:])

        db.session.add(user)

    db.session.commit()


def load_breeds():
    """ Loads in breeds from breed_data.txt. """

    print "Breeds"

    for row in open("seed_data/breed_data.txt"):
        row = row.rstrip().split('\t')
        name, descr, group, size, energy, url, pic = row
        group_obj = Group.query.filter(Group.name == group).one()

        breed = Breed(name=name, akc_url=url, group_id=group_obj.group_id,
                      size_id=size, energy_id=energy, description=descr, photo=pic)
        db.session.add(breed)

    db.session.commit()


def load_breeders():
    """ Loads in breeders from breeder_data.txt. """

    print "Breeders"

    bios = []
    names = []
    addys = []
    phs = []
    ems = []

    for row in open("seed_data/breeder_data.txt"):
        row = row.rstrip().split('\t')
        bio, name, addy, ph, em = row
        bios.append(bio)
        names.append(name)
        addys.append(addy)
        phs.append(ph)
        ems.append(em)

    for i in range(0, 100):
        all_users = set(user.user_id for user in User.query.all())
        all_breeders = set(breeder.breeder_id for breeder in Breeder.query.all())
        breeder_choices = list(all_users - all_breeders)
        breeder = Breeder(breeder_id=choice(breeder_choices), bio=choice(bios), name=choice(names), address=choice(addys), phone=choice(phs)[-13:], email=choice(ems))
        db.session.add(breeder)
        db.session.commit()


def load_new_litters():

    for breeder, breed in new_breeders_breeds.items():
        dam = Dog(name=choice(names_f), date_born=choice(date_borns_f), gender_id='f', description="I'm a cute dam!")
        sire = Dog(name=choice(names_m), date_born=choice(date_borns_m), gender_id='m', description="I'm a cute sire!")
        db.session.add(dam)
        db.session.add(sire)
        db.session.commit()
        date_born = choice(litter_dates)
        date_avail = date_born + timedelta(days=56)
        litter = Litter(breeder_id=breeder.breeder_id, breed_id=breed.breed_id, date_born=date_born, date_available=date_avail, description="A cute litter of puppies!", num_pups=choice(range(1, 16)), sire_id=sire.dog_id, dam_id=dam.dog_id)
        db.session.add(litter)
        db.session.commit()
        for i in range(0, litter.num_pups):
            pup = Pup(litter_id=litter.litter_id, name=choice(pup_names), available=choice([True, False]), gender_id=choice(['m', 'f']), description="I'm an adorable puppy!", price=choice(pup_prices))
            db.session.add(pup)
        db.session.commit()


def load_dogs():
    """ Loads in dogs from dog_data.txt. """

    print "Dogs"

    names_f = []
    date_borns_f = []

    litter_dates = []

    names_m = []
    date_borns_m = []

    litter_dates = []

    for row in open("seed_data/dog_f_data.txt"):
        row = row.rstrip().split('\t')
        name, date, gender = row
        date_born = datetime.strptime(date, "%m/%d/%Y")
        names_f.append(name)
        date_borns_f.append(date_born)
    for row in open("seed_data/dog_m_data.txt"):
        row = row.rstrip().split('\t')
        name, date, gender = row
        date_born = datetime.strptime(date, "%m/%d/%Y")
        names_m.append(name)
        date_borns_m.append(date_born)

    for row in open("seed_data/litter_data.txt"):
        row = row.rstrip().split('\t')
        date_born = datetime.strptime(row[0], "%m/%d/%Y")
        litter_dates.append(date_born)

    for breeder in Breeder.query.all():
        dogs_f = []
        dogs_m = []
        for litter in breeder.litters:
            dogs_f.append(litter.dam.dog_id)
            dogs_m.append(litter.sire.dog_id)
        if not dogs_f:
            dam1 = Dog(name=choice(names_f), date_born=choice(date_borns_f), gender_id='f', description="I'm a cute dam!")
            dam2 = Dog(name=choice(names_f), date_born=choice(date_borns_f), gender_id='f', description="I'm a cute dam!")
            db.session.add_all([dam1, dam2])
        if not dogs_m:
            sire1 = Dog(name=choice(names_m), date_born=choice(date_borns_m), gender_id='m', description="I'm a cute sire!")
            sire2 = Dog(name=choice(names_m), date_born=choice(date_borns_m), gender_id='m', description="I'm a cute sire!")
            db.session.add_all([sire1, sire2])

    breeders = [breeder.breeder_id for breeder in Breeder.query.all() if not breeder.litters]
    breeds = [breed.breed_id for breed in Breed.query.all()]

    free_sires = []
    free_dams = []

    for dog in Dog.query.all():
        if dog.gender_id == 'f':
            litters = [litter for litter in Litter.query.filter(Litter.dam_id == dog.dog_id)]
            if not litters:
                free_dams.append(dog)
        if dog.gender_id == 'm':
            litters = [litter for litter in Litter.query.filter(Litter.sire_id == dog.dog_id)]
            if not litters:
                free_sires.append(dog)

    for breeder in Breeder.query.all():
        for litter in breeder.litters:
            dam = Dog.query.get(litter.dam_id)
            if dam.gender_id == 'm':
                new_dam = free_dams.pop()
                litter.dam_id = new_dam.dog_id

    for breeder in Breeder.query.all():
        if not breeder.litters:
            breed = choice(breeds)
            date_born1 = choice(litter_dates)
            date_available1 = date_born + timedelta(days=56)
            sire1 = free_sires.pop()
            dam1 = free_dams.pop()
            litter1 = Litter(breeder_id=breeder.breeder_id, breed_id=breed, date_born=date_born1, date_available=date_available1, description="A cute litter of puppies!", num_pups=choice(range(1, 16)), sire_id=sire1.dog_id, dam_id=dam1.dog_id)
            date_born2 = choice(litter_dates)
            date_available2 = date_born + timedelta(days=56)
            sire2 = free_sires.pop()
            dam2 = free_dams.pop()
            litter2 = Litter(breeder_id=breeder.breeder_id, breed_id=breed, date_born=date_born2, date_available=date_available2, description="A cute litter of puppies!", num_pups=choice(range(1, 16)), sire_id=sire2.dog_id, dam_id=dam2.dog_id)
            db.session.add_all([litter1, litter2])


def load_litters():
    """ Loads in litters from litter_data.txt. """

    print "Litters"

    litter_dates = []

    breeds = Breed.query.all()
    # breeder_breeds = {breeder: choice(breeds) for breeder in Breeder.query.all()}
    # dog_breeds = {dog: choice(breeds) for dog in Dog.query.all()}

    breed_dogs = {breed: [] for breed in Breed.query.all()}
    for dog, breed in dog_breeds.items():
        breed_dogs[breed].append(dog)

    breed_breeders = {breed: [] for breed in Breed.query.all()}
    for breeder, breed in breeder_breeds.items():
        breed_breeders[breed].append(breeder)

    breeder_sires = {breeder: [] for breeder in breeder_breeds.keys()}
    breeder_dams = {breeder: [] for breeder in breeder_breeds.keys()}

    for dog, breed in dog_breeds.items():
        breeder = choice(breed_breeders[breed])
        if dog.gender_id == 'f':
            breeder_dams[breeder].append(dog)
        if dog.gender_id == 'm':
            breeder_sires[breeder].append(dog)

    for breed in breeds:
        if breed_breeders[breed]:
            breeder = choice(breed_breeders[breed])
            if breeder_sires[breeder]:
                sire = choice(breeder_sires[breeder])
                if breeder_dams[breeder]:
                    dam = choice(breeder_dams[breeder])
                    if sire and dam:
                        date_born = choice(litter_dates)
                        date_available = date_born + timedelta(days=56)
                        litter = Litter(breeder_id=breeder.breeder_id, breed_id=breed.breed_id, date_born=date_born, date_available=date_available, description="A cute litter of puppies!", num_pups=choice(range(1, 16)), sire_id=sire.dog_id, dam_id=dam.dog_id)
                        db.session.add(litter)
    db.session.commit()

    for row in open("seed_data/litter_data.txt"):
        row = row.rstrip().split('\t')
        date_born = datetime.strptime(row[0], "%m/%d/%Y")
        litter_dates.append(date_born)


def load_pups():
    """ Loads in puppies from pup_data.txt. """

    print "Pups"

    pup_names = []
    pup_prices = []

    for row in open("seed_data/pup_data.txt"):
        row = row.rstrip().split('\t')
        name, avail, gender, price = row
        pup_names.append(name)
        pup_prices.append(price)

    for litter in Litter.query.all():
        num = litter.num_pups
        for i in range(0, num):
            pup = Pup(litter_id=litter.litter_id, name=choice(names), available=choice([True, False]), gender_id=choice(['m', 'f']), description="I'm an adorable puppy!", price=choice(prices))
            db.session.add(pup)
    db.session.commit()


def load_awards():
    """ Loads in awards from award_data.txt. """

    print "Awards"

    names = []
    descrs = []
    dates = []

    for row in open("seed_data/award_data.txt"):
        row = row.rstrip().split('\t')
        name, descr, date_str = row
        date = datetime.strptime(date_str, "%m/%d/%Y")
        names.append(name)
        dates.append(date)
        descrs.append(descr)

    for breeder, sires in breeder_sires.items():
        if sires:
            for sire in sires:
                award = Award(breeder_id=breeder.breeder_id, dog_id=sire.dog_id, name=choice(names), description=choice(descrs), date=choice(dates))
                db.session.add(award)

    for breeder, dams in breeder_dams.items():
        if dams:
            for dam in dams:
                award = Award(breeder_id=breeder.breeder_id, dog_id=dam.dog_id, name=choice(names), description=choice(descrs), date=choice(dates))
                db.session.add(award)


def load_breeder_spots():
    """ Randomly generates breeder spots for users. """

    print "Breeder Spots"

    all_users = [i[0] for i in db.session.query(User.user_id).all()]
    all_breeders = [i[0] for i in db.session.query(Breeder.breeder_id).all()]
    non_breeders = [i for i in all_users if i not in all_breeders]

    for i in range(1, 1500):
        user_id = choice(non_breeders)
        breeder_id = choice(all_breeders)

        breeder_spot = BreederSpot(user_id=user_id, breeder_id=breeder_id)
        db.session.add(breeder_spot)

    db.session.commit()


def load_breed_spots():
    """ Randomnly generates breed spots for users. """

    print "Breed Spots"

    all_users = [i[0] for i in db.session.query(User.user_id).all()]
    all_breeders = [i[0] for i in db.session.query(Breeder.breeder_id).all()]
    non_breeders = [i for i in all_users if i not in all_breeders]

    for num in range(1, 1500):
        user_id = choice(non_breeders)
        breed_id = choice([i[0] for i in db.session.query(Breed.breed_id).all()])

        breed_spot = BreedSpot(user_id=user_id, breed_id=breed_id)
        db.session.add(breed_spot)

    db.session.commit()


def load_dogs_old():
    """ Loads in dogs from dog_f_data.txt and dog_m_data.txt. """

    print "Dogs"

    def load_dog_file(file_name, gender_id):
        for row in open(file_name):
            row = row.rstrip().split('\t')
            name, date, gender = row
            date_born = datetime.strptime(date, "%m/%d/%Y")

            dog = Dog(name=name, date_born=date_born, gender_id=gender_id,
                      description="I'm super cute.")
            db.session.add(dog)

        db.session.commit()

    load_dog_file("seed_data/dog_f_data.txt", 'f')
    load_dog_file("seed_data/dog_m_data.txt", 'm')


def load_litters_old():
    """ Loads in litters from litter_data.txt. """

    print "Litters"

    for row in open("seed_data/litter_data.txt"):
        row = row.rstrip().split('\t')
        date_born = datetime.strptime(row[0], "%m/%d/%Y")
        date_available = date_born + timedelta(days=56)
        num_pups = row[3]
        descr = 'so cute'
        breeder_id = choice([i[0] for i in db.session.query(Breeder.breeder_id).all()])
        breed_id = choice([i[0] for i in db.session.query(Breed.breed_id).all()])
        sire_id = choice([i[0] for i in db.session.query(Dog.dog_id)
                         .filter(Dog.gender_id == 'm').all()])
        dam_id = choice([i[0] for i in db.session.query(Dog.dog_id)
                         .filter(Dog.gender_id == 'f').all()])

        litter = Litter(breeder_id=breeder_id, breed_id=breed_id, date_born=date_born,
                        date_available=date_available, description=descr,
                        num_pups=num_pups, sire_id=sire_id, dam_id=dam_id)

        db.session.add(litter)

    db.session.commit()


def load_breedchars():
    """ Loads in breed chars from breedchar_data.txt. """

    print "BreedChars"

    for row in open("seed_data/breedchar_data.txt"):
        row = row.rstrip().split('\t')
        breed, char, descr = row
        breed_obj = Breed.query.filter(Breed.name == breed).one()
        char_obj = Char.query.filter(Char.char == char).one()

        breedchar = BreedChar(breed_id=breed_obj.breed_id, char_id=char_obj.char_id,
                              description=descr)
        db.session.add(breedchar)

    db.session.commit()


def load_events():
    """ Loads in events from event_data.txt. """

    print "Events"

    names = []
    descrs = []
    dates = []

    for row in open("seed_data/event_data.txt"):
        row = row.rstrip().split('\t')
        name, descr, date_str = row
        date = datetime.strptime(date_str, "%m/%d/%Y")
        names.append(name)
        descrs.append(descr)
        dates.append(date)

    for breeder in Breeder.query.all():
        if not breeder.events:
            event1 = Event(breeder_id=breeder.breeder_id, name=choice(names), description=choice(descrs), date=choice(dates))
            event2 = Event(breeder_id=breeder.breeder_id, name=choice(names), description=choice(descrs), date=choice(dates))
            db.session.add_all([event1, event2])

    db.session.commit()


def load_awards_new():
    """ Loads in awards from award_data.txt. """

    print "Awards"

    names = []
    ds = []
    dates = []

    for row in open("seed_data/award_data.txt"):
        row = row.rstrip().split('\t')
        name, descr, date_str = row
        date = datetime.strptime(date_str, "%m/%d/%Y")
        names.append(name)
        ds.append(descr)
        dates.append(date)

    for breeder in Breeder.query.all():
        dogs = []
        for litter in breeder.litters:
            dogs.append(litter.dam.dog_id)
            dogs.append(litter.sire.dog_id)
        if dogs:
            if not breeder.awards:
                award1 = Award(breeder_id=breeder.breeder_id, dog_id=choice(dogs), name=choice(names), description=choice(ds), date=choice(dates))
                award2 = Award(breeder_id=breeder.breeder_id, dog_id=choice(dogs), name=choice(names), description=choice(ds), date=choice(dates))
                award3 = Award(breeder_id=breeder.breeder_id, dog_id=choice(dogs), name=choice(names), description=choice(ds), date=choice(dates))
                db.session.add_all([award1, award2, award3])

    db.session.commit()


def load_blog_posts():
    """ Loads in blog posts from blog_data.txt. """

    print "Blog Posts"

    for row in open("seed_data/blog_data.txt"):
        row = row.rstrip().split('\t')
        cat, post, date_str = row
        date = datetime.strptime(date_str, "%m/%d/%Y")
        breeder_id = choice([i[0] for i in db.session.query(Breeder.breeder_id).all()])

        blog = Blog(breeder_id=breeder_id, date=date, category=cat, post=post)
        db.session.add(blog)

    db.session.commit()


def load_breeder_photo():
    """ Loads in photo captions from photo_data.txt. """

    print "Breeder Photos"

    captions = []

    for row in open("seed_data/photo_data.txt"):
        row = row.rstrip().split('\t')
        p, caption = row
        captions.append(caption)

    for breeder in Breeder.query.all():
        if not breeder.photos:
                photo1 = BreederPhoto(breeder_id=breeder.breeder_id, photo='https://unsplash.it/400/400/?random', caption=choice(captions))
                photo2 = BreederPhoto(breeder_id=breeder.breeder_id, photo='https://unsplash.it/400/400/?random', caption=choice(captions))
                photo3 = BreederPhoto(breeder_id=breeder.breeder_id, photo='https://unsplash.it/400/400/?random', caption=choice(captions))
                db.session.add_all([photo1, photo2, photo3])

    db.session.commit()


def load_dog_photo():
    """ Loads in photo captions from photo_data.txt. """

    print "Dog Photos"

    captions = []

    for row in open("seed_data/photo_data.txt"):
        row = row.rstrip().split('\t')
        p, caption = row
        captions.append(caption)

    for dog in Dog.query.all():
        if len(dog.photos) == 1:
            photo1 = DogPhoto(dog_id=dog.dog_id, photo='http://www.randomdoggiegenerator.com/randomdoggie.php', caption=choice(captions))
            photo2 = DogPhoto(dog_id=dog.dog_id, photo='http://www.randomdoggiegenerator.com/randomdoggie.php', caption=choice(captions))
            db.session.add_all([photo1, photo2])

    db.session.commit()


def load_event_photo():
    """ Loads in photo captions from photo_data.txt. """

    print "Event Photos"

    captions = []

    for row in open("seed_data/photo_data.txt"):
        row = row.rstrip().split('\t')
        p, caption = row
        captions.append(caption)

    for event in Event.query.all():
        if not event.photos:
            photo1 = EventPhoto(event_id=event.event_id, photo='https://unsplash.it/400/400/?random', caption=choice(captions))
            photo2 = EventPhoto(event_id=event.event_id, photo='https://unsplash.it/400/400/?random', caption=choice(captions))
            photo3 = EventPhoto(event_id=event.event_id, photo='https://unsplash.it/400/400/?random', caption=choice(captions))
            db.session.add_all([photo1, photo2, photo3])

    db.session.commit()


def load_litter_photo():
    """ Loads in photo captions from photo_data.txt. """

    print "Litter Photos"

    for row in open("seed_data/photo_data.txt"):
        row = row.rstrip().split('\t')
        p, caption = row
        litter_id = choice([i[0] for i in db.session.query(Litter.litter_id).all()])
        photo = 'http://www.randomdoggiegenerator.com/randomdoggie.php'

        l_photo = LitterPhoto(litter_id=litter_id, photo=photo, caption=caption)
        db.session.add(l_photo)

    db.session.commit()


def load_pup_photo():
    """ Loads in photo captions from photo_data.txt. """

    print "Pup Photos"

    captions = []

    for row in open("seed_data/photo_data.txt"):
        row = row.rstrip().split('\t')
        p, caption = row
        captions.append(caption)

    for pup in Pup.query.all():
        if not pup.photos:
            photo1 = PupPhoto(pup_id=pup.pup_id, photo='http://www.randomdoggiegenerator.com/randomdoggie.php', caption=choice(captions))
            photo2 = PupPhoto(pup_id=pup.pup_id, photo='http://www.randomdoggiegenerator.com/randomdoggie.php', caption=choice(captions))        
            db.session.add_all([photo1, photo2])

    db.session.commit()


def more_pups_old():
    """ adds pups to litters where num_pups does not correspond. """

    print "more pups"

    for litter in Litter.query.all():
        pups_needed = litter.num_pups - len(litter.pups)
        if pups_needed > 0:
            for i in range(0, pups_needed):
                gender_id = choice(['m', 'f'])
                name = choice([pup.name for pup in Pup.query.all() if pup.gender_id == gender_id])
                available = choice([True, False])
                description = "i'm really really cute!"
                price = randint(300, 10000)
                new_pup = Pup(litter_id=litter.litter_id,
                              name=name,
                              available=available,
                              gender_id=gender_id,
                              description=description,
                              price=price)
                db.session.add(new_pup)
            db.session.commit()


def fix_addresses():
    """ fixes breeder addresses so that they are real, for google maps. """

    print "fixing addresses"

    breeders = Breeder.query.all()
    counter = -1
    for row in open("seed_data/new_addy.txt"):
        row = row.rstrip()
        addys.append(row)
        counter += 1
        breeders[counter].address = row
    db.session.commit()

    for breed in Breed.query.all():
        addys = []
        for row in open("seed_data/new_addy.txt"):
            row = row.rstrip()
            addys.append(row)
        breeders = list({litter.breeder for litter in breed.litters})
        for breeder in breeders:
            breeder.address = addys.pop(randint(0, len(addys) - 1))



def fix_dogs_old():
    """ fixes dogs that are in multiple litters. """

    print "fixing dogs"

    breeds = Breed.query.all()

    all_dams = [dog for dog in Dog.query.filter(Dog.gender_id == 'f').all()]
    dam_breeds = {}
    for dam in all_dams:
        rando_breed = choice(breeds)
        dam_breeds[dam] = rando_breed

    for dam, breed in dam_breeds.items():
        for litter in db.session.query(Litter).filter(Litter.dam_id == dam.dog_id).all():
            if litter.breed != breed:
                litter.breed = breed

    all_sires = [dog for dog in Dog.query.filter(Dog.gender_id == 'm').all()]
    sire_breeds = {}
    for sire in all_sires:
        rando_breed = choice(breeds)
        sire_breeds[sire] = rando_breed

    for sire, breed in sire_breeds.items():
        for litter in db.session.query(Litter).filter(Litter.sire_id == sire.dog_id).all():
            if litter.breed != breed:
                litter.breed = breed

    db.session.commit()


###############################################################################

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
    # load_users()
    # load_breeders()
    # load_breeds()
    # load_dogs()
    # load_dogs()


    # load_breeder_spots()
    # load_breed_spots()

    # load_litters()
    # load_pups()
    # load_pups()
    # load_pups()
    # load_pups()
    # load_breedchars()

    #to fix the # of pups in the db (to match litter size)
    # more_pups()

    #to fix the addresses to be real (so that recognized by google maps)
    # fix_addresses()

    # These run mult times to make plenty of photos/events/awards for each
    # load_events()
    # load_events()
    # load_events()

    # load_awards()
    # load_awards()
    # load_awards()

    # load_blog_posts()
    # load_blog_posts()
    # load_blog_posts()

    # load_breeder_photo()
    # load_breeder_photo()
    # load_breeder_photo()

    # load_dog_photo()
    # load_dog_photo()
    # load_dog_photo()

    # load_event_photo()
    # load_event_photo()
    # load_event_photo()

    # load_litter_photo()
    # load_litter_photo()
    # load_litter_photo()

    # load_pup_photo()
    # load_pup_photo()
    # load_pup_photo()
