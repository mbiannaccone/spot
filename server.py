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

    return render_template("homepage.html",
                           groups=groups,
                           sizes=sizes,
                           energies=energies,
                           chars=chars,
                           breeds=breeds)


@app.route('/register')
def register():
    """ Renders register template form. """

    return render_template('register.html')


@app.route('/register', methods=["POST"])
def register_process():
    """ Checks if email already exists, and if not creates a new user. """

    email = request.form.get("email")
    pwd = request.form.get("pwd")
    zipcode = request.form.get("zip")

    if db.session.query(User).filter(User.email == email).first() is None:
        new_user = User(email=email, password=pwd, zipcode=zipcode)
        db.session.add(new_user)
        db.session.commit()
        flash("Logged in as %s" % email)
        session['user_id'] = new_user.user_id
        return redirect('/user/%s' % new_user.user_id)
    else:
        flash("A user account with that email already exists, please login.")
        return redirect('/login')


@app.route('/login')
def login_page():
    """ Renders login page. """
    return render_template('/login.html')


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
        return redirect('/user/%s' % user.user_id)


@app.route("/logout")
def logout_process():
    """Logs out current user."""

    del session['user_id']
    flash("You are now logged out. Goodbye!")

    return redirect("/")


@app.route('/user/<user_id>')
def user_profile(user_id):
    """ User's profile page. """

    print 'hi im in the user page.'
    return redirect('/')


@app.route('/breed-search')
def breed_search():
    """ Breed search results. """

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
                if keyword in breed_char.description:
                    search[breed_char.breed] += 1
            for breed in Breed.query.all():
                if keyword in breed.description:
                    search[breed] += 1

        search_results = [(result, breed) for breed, result in search.items() if result != 0]
        search_results.sort(reverse=True)

    return render_template('breed-search.html', search_results=search_results)


@app.route('/breeds/<breed_id>')
def breed_info(breed_id):
    """ Renders a breed's info page. """

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
                           breed_chars=breed_chars)


@app.route('/breeder-search')
def breeder_search():
    """ Breeder search results. """

    location = request.args.get("location")
    breed = int(request.args.get('breed'))

    breeders = db.session.query(Breeder).join(Litter, Breed).filter(Breed.breed_id == breed)

    return render_template('breeder-search.html', breeders=breeders, breed=Breed.query.get(breed))


@app.route('/breeders/<breeder_id>')
def breeder_info(breeder_id):
    """ Renders a breeder's info page. """

    breeder = Breeder.query.get(breeder_id)
    photos = breeder.photos
    litters = [(litter, litter.breed) for litter in breeder.litters]
    events = breeder.events
    dogs = [(Dog.query.get(litter.sire_id),
            Dog.query.get(litter.dam_id)) for litter in breeder.litters]
    awards = [(award, award.dog) for award in breeder.awards]
    blogs = breeder.blogs

    return render_template('breeder-info.html', breeder=breeder, photos=photos,
                           litters=litters, events=events, dogs=dogs,
                           awards=awards, blogs=blogs)


@app.route('/breeders/<breeder_id>/litters/<litter_id>')
def litter_info(breeder_id, litter_id):
    """ Renders a litter's info page. """

    breeder = Breeder.query.get(breeder_id)
    litter = Litter.query.get(litter_id)
    breed = litter.breed
    sire = Dog.query.get(litter.sire_id)
    dam = Dog.query.get(litter.dam_id)
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
                           photos=photos)


@app.route('/breeders/<breeder_id>/dogs/<dog_id>')
def dog_info(breeder_id, dog_id):
    """ Renders a dog's info page. """

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
                           breed=breed)


@app.route('/breeders/<breeder_id>/events/<event_id>')
def event_info(breeder_id, event_id):
    """ Render's a breeder event's info page. """

    breeder = Breeder.query.get(breeder_id)
    event = Event.query.get(event_id)
    photos = event.photos

    return render_template('event-info.html',
                           breeder=breeder,
                           event=event,
                           photos=photos)


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
