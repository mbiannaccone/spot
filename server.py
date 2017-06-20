""" Spot's server! """

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session,
                   jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime, timedelta
from model import (Award, Blog, Breed, BreedChar, Breeder, BreederPhoto, PupPhoto,
                   Dog, DogPhoto, Energy, Event, EventPhoto, Gender, Group, Pup,
                   Litter, LitterPhoto, Char, Size, User, BreedSpot, BreederSpot)
from model import Addy
from model import connect_to_db, db
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
import bcrypt

app = Flask(__name__)

app.secret_key = "key"
app.jinja_env.undefined = StrictUndefined


def check_user():
    """ Checks if a user is logged in. """

    if 'user_id' in session:
        return User.query.get(session['user_id'])
    else:
        return None


@app.route('/')
def index():
    """ Homepage. """

    sizes = Size.query.all()
    groups = Group.query.all()
    energies = Energy.query.all()
    chars = Char.query.filter(Char.char_id > 12).all()
    breeds = Breed.query.all()

    user = check_user()

    return render_template("homepage.html",
                           groups=groups,
                           sizes=sizes,
                           energies=energies,
                           chars=chars,
                           breeds=breeds,
                           user=user)


@app.route('/register')
def register():
    """ Renders register template form. """

    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        flash("You're already logged in as %s!" % user.email)
        flash("If you'd like to register with a new email, please log out first.")
        return redirect('/users/%s' % user.user_id)
    else:
        user = None

    return render_template('register.html', user=user)


@app.route('/register', methods=["POST"])
def register_process():
    """ Checks if email already exists, and if not creates a new user. """

    email = request.form.get("email")
    zipcode = request.form.get("zip")
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    phone = request.form.get("phone")
    pwd = request.form.get("pwd")

    if db.session.query(User).filter(User.email == email).first() is None:
        new_user = User(email=email, password=pwd, zipcode=zipcode)
        if fname:
            new_user.fname = fname
        if lname:
            new_user.lname = lname
        if phone:
            new_user.phone = phone
        db.session.add(new_user)
        db.session.commit()
        flash("Logged in as %s" % email)
        session['user_id'] = new_user.user_id
        return redirect('/users/%s' % new_user.user_id)
    else:
        flash("A user account with that email already exists, please login.")
        return redirect('/login')


@app.route('/login')
def login_page():
    """ Renders login page. """

    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        flash("You're already logged in as %s!" % user.email)
        return redirect('/users/%s' % user.user_id)
    else:
        user = None

    return render_template('/login.html', user=user)


@app.route('/login', methods=['POST'])
def login_process():
    """ Checks if email/pwd are correct and redirects to profile. """

    email = request.form.get("email")
    pwd = request.form.get("pwd")

    if db.session.query(User).filter(User.email == email, User.password == pwd
                                     ).first() is None:
        flash("Email/password combination do not match.")
        return redirect('/login')
    else:
        flash("Logged in as %s" % email)
        user = User.query.filter(User.email == email).one()
        session['user_id'] = user.user_id
        return redirect('/users/%s' % user.user_id)


@app.route("/logout")
def logout_process():
    """Logs out current user."""

    del session['user_id']
    flash("You are now logged out. Goodbye!")

    return redirect("/")


@app.route('/users/<user_id>')
def user_profile(user_id):
    """ User's profile page. """

    if 'user_id' not in session:
        flash("Please log in first!")
        return redirect('/login')
    else:
        user = User.query.get(session['user_id'])
        breed_spots = [breed_spot.breed for breed_spot in user.breed_spots]
        breed_spots.reverse()
        breeder_spots = [(breeder_spot.breeder, breeder_spot.breeder.litters) for breeder_spot in user.breeder_spots]
        breeder_spots.reverse()
        date_filter = datetime.now() - timedelta(days=120)
        return render_template('user-info.html',
                               user=user,
                               breed_spots=breed_spots,
                               breeder_spots=breeder_spots,
                               date_filter=date_filter)


@app.route('/user-updates', methods=['POST'])
def update_user_info():
    """ Updates user's profile information. """

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")
    current_pwd = request.form.get("current_pwd")
    zipcode = request.form.get("zipcode")
    phone = request.form.get("phone")
    user_id = request.form.get("user")

    user = User.query.get(user_id)

    updated_info = []

    if current_pwd != user.password:
        updated_info.append("Did NOT make any updates as password entry does not match current password, please try again.")
    else:
        if fname and fname != user.fname:
            user.fname = fname
            updated_info.append('First Name')
        if lname and lname != user.lname:
            user.lname = lname
            updated_info.append('Last Name')
        if email and email != user.email:
            user.email = email
            updated_info.append('Email')
        if zipcode and zipcode != user.zipcode:
            user.zipcode = zipcode
            updated_info.append('Zipcode')
        if phone and phone != user.phone:
            user.phone = phone
            updated_info.append('Phone')
        if password and password != user.password:
            user.password = password
            updated_info.append('Password')

    db.session.commit()

    return 'Sucessfully updated the following info:\n - ' + '\n - '.join(updated_info)


def breed_search_rank(size_id, group_id, energy_id, keyword, chars):
    """ Takes in search filters and ranks the search results. """

    search = {breed: 0 for breed in Breed.query.all()}

    def add_char_value(class_id, class_name):
        if class_id:
            for breed in class_name.query.get(class_id).breeds:
                search[breed] += 25

    add_char_value(size_id, Size)
    add_char_value(group_id, Group)
    add_char_value(energy_id, Energy)

    if chars:
        for char_id in chars:
            for breed_char in Char.query.get(char_id).breed_chars:
                search[breed_char.breed] += 25

    if keyword:
        for breed_char in BreedChar.query.all():
            if keyword.lower() in breed_char.description.lower():
                search[breed_char.breed] += 1
        for breed in Breed.query.all():
            if keyword.lower() in breed.description.lower():
                search[breed] += 1
        for breed in Breed.query.all():
            if keyword.lower() in breed.name.lower():
                search[breed] += 25

    search_results = [(result, breed) for breed, result in search.items() if result != 0]
    search_results.sort(reverse=True)

    return search_results


@app.route('/breed-search')
def breed_search():
    """ Breed search results. """

    user = check_user()

    if "search all" in request.args:
        search_results = [(1, breed) for breed in Breed.query.all()]

    else:
        size_id = request.args.get('size')
        group_id = request.args.get('group')
        energy_id = request.args.get('energy')
        keyword = request.args.get('keyword')

        chars = []
        for char in Char.query.filter(Char.char_id > 12).all():
            value = request.args.get(str(char.char_id))
            if value:
                chars.append(int(value))

        search_results = breed_search_rank(size_id,
                                           group_id,
                                           energy_id,
                                           keyword,
                                           chars)

    return render_template('breed-search.html',
                           search_results=search_results,
                           user=user)


@app.route('/breeds/<breed_id>')
def breed_info(breed_id):
    """ Renders a breed's info page. """

    user = check_user()

    breed = Breed.query.get(breed_id)
    group = breed.group
    size = breed.size
    energy = breed.energy

    breed_chars = [(breed_char.char_id,
                    Char.query.get(breed_char.char_id),
                    breed_char
                    ) for breed_char in breed.breed_chars if (
                   breed_char.char_id in [3, 4, 5, 6, 7, 9])]
    breed_chars.sort()

    fun_chars = [(breed_char.char_id,
                  Char.query.get(breed_char.char_id),
                  breed_char
                  ) for breed_char in breed.breed_chars if (
                 breed_char.char_id not in [3, 4, 5, 6, 7, 9])]
    fun_chars.sort()

    spots = breed.breed_spots
    users_spots = [spot.user for spot in spots]

    return render_template('breed-info.html',
                           breed=breed,
                           group=group,
                           size=size,
                           energy=energy,
                           breed_chars=breed_chars,
                           fun_chars=fun_chars,
                           user=user,
                           spots=spots,
                           users_spots=users_spots)


def breeder_search_rank(geo_location, breeders):
    """ Ranks breeder search results according to distance to location. """

    dist_breeders = []

    for breeder in breeders:
        geo = Addy.query.filter(breeder.address == Addy.addys).first()
        dist = vincenty((geo.lat, geo.long), (geo_location.latitude, geo_location.longitude)).miles
        dist_breeders.append((dist, breeder))
        dist_breeders.sort()

    return dist_breeders


@app.route('/breeder-search')
def breeder_search():
    """ Breeder search results. """

    user = check_user()

    location = request.args.get("location")
    if not location:
        location = user.zipcode

    geolocator = Nominatim()
    geo_location = geolocator.geocode(location)

    breed = request.args.get('breed')

    breeders = db.session.query(Breeder
                                ).join(Litter, Breed
                                       ).filter(Breed.breed_id == breed).all()

    dist_breeders = breeder_search_rank(geo_location, breeders)

    return render_template('breeder-search.html',
                           breeders=dist_breeders,
                           breed=Breed.query.get(breed),
                           user=user,
                           location=location)


@app.route('/breeders/<breeder_id>')
def breeder_info(breeder_id):
    """ Renders a breeder's info page. """

    user = check_user()

    breeder = Breeder.query.get(breeder_id)
    photos = breeder.photos
    litters = [(litter.date_born, litter, litter.breed) for litter in breeder.litters]
    litters.sort(reverse=True)
    breeds = list({breed for date, litter, breed in litters})
    events = [(event.date, event) for event in breeder.events]
    events.sort(reverse=True)
    sires = list({Dog.query.get(litter.sire_id) for litter in breeder.litters})
    dams = list({Dog.query.get(litter.dam_id) for litter in breeder.litters})
    awards = [(award.date, award, award.dog) for award in breeder.awards]
    awards.sort(reverse=True)
    blogs = [(blog.date, blog) for blog in breeder.blogs]
    blogs.sort(reverse=True)
    spots = breeder.breeder_spots
    users_spots = [spot.user for spot in spots]

    return render_template('breeder-info.html',
                           breeder=breeder,
                           photos=photos,
                           litters=litters,
                           events=events,
                           sires=sires,
                           dams=dams,
                           awards=awards,
                           blogs=blogs,
                           user=user,
                           breeds=breeds,
                           spots=spots,
                           users_spots=users_spots)


@app.route('/breeders/<breeder_id>/litters/<litter_id>')
def litter_info(breeder_id, litter_id):
    """ Renders a litter's info page. """

    user = check_user()

    breeder = Breeder.query.get(breeder_id)
    litter = Litter.query.get(litter_id)
    breed = litter.breed
    sire = litter.sire
    dam = litter.dam
    f_pups = [(pup.available, pup) for pup in litter.pups if pup.gender_id == 'f']
    m_pups = [(pup.available, pup) for pup in litter.pups if pup.gender_id == 'm']
    f_pups.sort(reverse=True)
    m_pups.sort(reverse=True)
    photos = litter.photos
    spots = breeder.breeder_spots
    users_spots = [spot.user for spot in breeder.breeder_spots]

    return render_template('litter-info.html',
                           breeder=breeder,
                           litter=litter,
                           breed=breed,
                           sire=sire,
                           dam=dam,
                           f_pups=f_pups,
                           m_pups=m_pups,
                           photos=photos,
                           user=user,
                           spots=spots,
                           users_spots=users_spots)


@app.route('/breeders/<breeder_id>/dogs/<dog_id>')
def dog_info(breeder_id, dog_id):
    """ Renders a dog's info page. """

    user = check_user()

    breeder = Breeder.query.get(breeder_id)
    dog = Dog.query.get(dog_id)
    awards = [(award.date, award) for award in dog.awards]
    photos = dog.photos
    litters = Litter.query.filter((Litter.dam_id == dog.dog_id) |
                                  (Litter.sire_id == dog.dog_id)
                                  ).order_by(Litter.date_born.desc()).all()
    breed = litters[0].breed
    spots = breeder.breeder_spots
    users_spots = [spot.user for spot in breeder.breeder_spots]

    return render_template('dog-info.html',
                           breeder=breeder,
                           dog=dog,
                           awards=awards,
                           photos=photos,
                           litters=litters,
                           breed=breed,
                           user=user,
                           spots=spots,
                           users_spots=users_spots)


@app.route('/breed-spot', methods=["POST"])
def spot_breed():
    """ Adds breed to the user's list of spots. """

    if 'user_id' not in session:
        flash("Please log in first!")
        return redirect('/login')
    else:
        user = User.query.get(session['user_id'])
        breed_id = request.form.get("breed")
        breed = Breed.query.get(breed_id)

        breedspot = BreedSpot(user_id=user.user_id, breed_id=breed_id)
        db.session.add(breedspot)
        db.session.commit()
        flash("You've spotted the %s breed!" % breed.name)
    return redirect('/breeds/%s' % breed_id)


@app.route('/remove-breed-spot', methods=["POST"])
def remove_breed_spot():
    """ Removes breed from user's list of spots. """

    user_id = session['user_id']
    breed_id = request.form.get('breed')
    breed = Breed.query.get(breed_id)

    breed_spot = BreedSpot.query.filter(BreedSpot.breed_id == breed_id,
                                        BreedSpot.user_id == user_id).first()
    db.session.delete(breed_spot)
    db.session.commit()
    flash("You've unspotted the %s breed." % breed.name)

    if request.form.get('user-page'):
        return redirect('/users/%s' % user_id)

    return redirect('/breeds/%s' % breed_id)


@app.route('/breeder-spot', methods=["POST"])
def spot_breeder():
    """ Adds breeder to the user's list of spots. """

    if 'user_id' not in session:
        flash("Please log in first!")
        return redirect('/login')
    else:
        user = User.query.get(session['user_id'])
        breeder_id = request.form.get('breeder')
        breeder = Breeder.query.get(breeder_id)

        breederspot = BreederSpot(user_id=user.user_id, breeder_id=breeder_id)
        db.session.add(breederspot)
        db.session.commit()
        flash("You've spotted this breeder: %s" % breeder.name)
    return redirect('/breeders/%s' % breeder_id)


@app.route('/remove-breeder-spot', methods=["POST"])
def remove_breeder_spot():
    """ Removes breeder from user's list of spots. """

    user_id = session['user_id']
    breeder_id = request.form.get('breeder')
    breeder = Breeder.query.get(breeder_id)

    breeder_spot = BreederSpot.query.filter(BreederSpot.breeder_id == breeder_id,
                                            BreederSpot.user_id == user_id
                                            ).first()
    db.session.delete(breeder_spot)
    db.session.commit()
    flash("You've unspotted this breeder: %s" % breeder.name)

    if request.form.get('user-page'):
        return redirect('/users/%s' % user_id)

    return redirect('/breeders/%s' % breeder_id)


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
