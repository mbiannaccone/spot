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
        print 'got to if'
        return redirect('/login')
    else:
        print 'got to else'
        flash("Logged in! as %s" % email)
        user = User.query.filter(User.email == email).one()
        session['user_id'] = user.user_id
        return redirect('/user/%s' % user.user_id)


@app.route('/user/<user_id>')
def user_profile(user_id):
    """ User's profile page. """

    print 'hi im in the user page.'


@app.route('/breed-search')
def breed_search():
    """ Breed search results. """
    pass


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
