""" Spot's server! """

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session,
                   jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime
from model import (Award, Blog, Breed, BreedChar, Breeder, BreederPhoto, PupPhoto,
                   Dog, DogPhoto, Energy, Event, EventPhoto, Gender, Group, Pup,
                   Litter, LitterPhoto, Char, Size, User, BreedSpot, BreederSpot)
from model import connect_to_db, db

app = Flask(__name__)

app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """ Homepage. """

    sizes = Size.query.all()
    groups = Group.query.all()
    energies = Energy.query.all()
    chars = Char.query.filter(Char.char_id > 12).all()
    breeds = Breed.query.all()

    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    else:
        user = None

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
        flash("You're already logged in as %s! If you'd like to register with a new email, please log out first." % user.email)
        return redirect('/users/%s' % user.user_id)
    else:
        user = None

    return render_template('register.html', user=user)


@app.route('/register', methods=["POST"])
def register_process():
    """ Checks if email already exists, and if not creates a new user. """

    email = request.form.get("email")
    pwd = request.form.get("pwd")
    zipcode = request.form.get("zip")
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    phone = request.form.get("phone")

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
        user = User.query.get(user_id)
        breed_spots = list({breed_spot.breed for breed_spot in user.breed_spots})
        breeder_spots = list({breeder_spot.breeder for breeder_spot in user.breeder_spots})
        return render_template('user-info.html',
                               user=user,
                               breed_spots=breed_spots,
                               breeder_spots=breeder_spots)


@app.route('/breed-search')
def breed_search():
    """ Breed search results. """

    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    else:
        user = None

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

        search = {breed: 0 for breed in Breed.query.all()}

        if size_id:
            for breed in Size.query.get(size_id).breeds:
                search[breed] += 25

        if group_id:
            for breed in Group.query.get(group_id).breeds:
                search[breed] += 25

        if energy_id:
            for breed in Energy.query.get(energy_id).breeds:
                search[breed] += 25

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

    return render_template('breed-search.html', search_results=search_results, user=user)


@app.route('/breeds/<breed_id>')
def breed_info(breed_id):
    """ Renders a breed's info page. """

    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    else:
        user = None

    breed = Breed.query.get(breed_id)
    group = breed.group
    size = breed.size
    energy = breed.energy
    breed_chars = [(breed_char.char_id,
                    Char.query.get(breed_char.char_id),
                    breed_char,) for breed_char in breed.breed_chars]
    breed_chars.sort()

    return render_template('breed-info.html',
                           breed=breed,
                           group=group,
                           size=size,
                           energy=energy,
                           breed_chars=breed_chars,
                           user=user)


@app.route('/breeder-search')
def breeder_search():
    """ Breeder search results. """

    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    else:
        user = None

    location = request.args.get("location")

    if "search all" in request.args:
        breeders = Breeder.query.all()[:10]
        return render_template('breeder-search.html',
                               breeders=breeders,
                               breed=None,
                               user=user,
                               location=location)

    else:
        breed = int(request.args.get('breed'))
        breeders = db.session.query(Breeder).join(Litter, Breed).filter(Breed.breed_id == breed)
        return render_template('breeder-search.html',
                               breeders=breeders,
                               breed=Breed.query.get(breed),
                               user=user,
                               location=location)


@app.route('/breeders/<breeder_id>')
def breeder_info(breeder_id):
    """ Renders a breeder's info page. """

    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    else:
        user = None

    breeder = Breeder.query.get(breeder_id)
    photos = breeder.photos
    litters = [(litter, litter.breed) for litter in breeder.litters]
    breeds = list({breed for litter, breed in litters})
    events = breeder.events
    sires = list({Dog.query.get(litter.sire_id) for litter in breeder.litters})
    dams = list({Dog.query.get(litter.dam_id) for litter in breeder.litters})
    awards = [(award, award.dog) for award in breeder.awards]
    blogs = breeder.blogs

    return render_template('breeder-info.html', breeder=breeder, photos=photos,
                           litters=litters, events=events, sires=sires, dams=dams,
                           awards=awards, blogs=blogs, user=user, breeds=breeds)


@app.route('/breeders/<breeder_id>/litters/<litter_id>')
def litter_info(breeder_id, litter_id):
    """ Renders a litter's info page. """

    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    else:
        user = None

    breeder = Breeder.query.get(breeder_id)
    litter = Litter.query.get(litter_id)
    breed = litter.breed
    sire = litter.sire
    dam = litter.dam
    f_pups = [(pup, pup.photos) for pup in litter.pups if pup.gender_id == 'f']
    m_pups = [(pup, pup.photos) for pup in litter.pups if pup.gender_id == 'm']
    photos = litter.photos

    return render_template('litter-info.html',
                           breeder=breeder,
                           litter=litter,
                           breed=breed,
                           sire=sire,
                           dam=dam,
                           f_pups=f_pups,
                           m_pups=m_pups,
                           photos=photos,
                           user=user)


@app.route('/breeders/<breeder_id>/dogs/<dog_id>')
def dog_info(breeder_id, dog_id):
    """ Renders a dog's info page. """

    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    else:
        user = None

    breeder = Breeder.query.get(breeder_id)
    dog = Dog.query.get(dog_id)
    awards = dog.awards
    photos = dog.photos
    litters = Litter.query.filter((Litter.dam_id == dog.dog_id) |
                                  (Litter.sire_id == dog.dog_id)).all()
    breed = litters[0].breed

    return render_template('dog-info.html',
                           breeder=breeder,
                           dog=dog,
                           awards=awards,
                           photos=photos,
                           litters=litters,
                           breed=breed,
                           user=user)


@app.route('/breeders/<breeder_id>/events/<event_id>')
def event_info(breeder_id, event_id):
    """ Render's a breeder event's info page. """

    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    else:
        user = None

    breeder = Breeder.query.get(breeder_id)
    event = Event.query.get(event_id)
    photos = event.photos

    return render_template('event-info.html',
                           breeder=breeder,
                           event=event,
                           photos=photos,
                           user=user)


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


@app.route('/breeder-spot', methods=["POST"])
def spot_breeder():
    """ Adds breeder to the user's list of spots. """

    if 'user_id' not in session:
        flash("Please log in first!")
        return redirect('/login')
    else:
        user = User.query.get(session['user_id'])
        breeder_id = request.form.get("breeder")
        breeder = Breeder.query.get(breeder_id)

        breederspot = BreederSpot(user_id=user.user_id, breeder_id=breeder_id)
        db.session.add(breederspot)
        db.session.commit()
        flash("You've spotted this breeder: %s" % breeder.name)
    return redirect('/breeders/%s' % breeder_id)


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
