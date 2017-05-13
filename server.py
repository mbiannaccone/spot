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

    return render_template("homepage.html",
                           groups=groups,
                           sizes=sizes,
                           energies=energies,
                           chars=chars)


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

    size_id = request.args.get('size')
    group_id = request.args.get('group')
    energy_id = request.args.get('energy')

    print size_id

    chars = []
    for char in Char.query.filter(Char.char_id > 12).all():
        print char
        print char.char_id
        value = request.args.get(str(char.char_id))
        if value:
            chars.append(int(value))
    print chars

    search_results = {}

    if size_id:
        for breed in Size.query.get(size_id).breeds:
            search_results[breed] = 5

    if group_id:
        for breed in Group.query.get(group_id).breeds:
            if breed not in search_results:
                search_results[breed] = 0
            search_results[breed] += 5

    if energy_id:
        for breed in Energy.query.get(energy_id).breeds:
            if breed not in search_results:
                search_results[breed] = 0
            search_results[breed] += 5

    if chars:
        for char_id in chars:
            for breed_char in Char.query.get(char_id).breed_chars:
                if breed_char.breed not in search_results:
                    search_results[breed_char.breed] = 0
                search_results[breed_char.breed] += 5

    return render_template('breed-search.html', search_results=search_results)


@app.route('/breed-search/<breed_id>')
def breed_info(breed_id):
    """ A breed's info page. """
    pass


@app.route('/breeder-search')
def breeder_search():
    """ Breeder search results. """
    pass


@app.route('/breeder-search/<breeder_id>')
def breeder_info(breed_id):
    pass


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
