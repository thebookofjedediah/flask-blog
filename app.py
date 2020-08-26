"""Blogly application."""

from flask import Flask, render_template
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = "mysecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def get_users():
    """shows list of all users"""
    users = User.query.all()
    return render_template('list.html', users=users)

@app.route('/<int:user_id>')
def user_details(user_id):
    """show details about user"""
    user = User.query.get(user_id)
    return render_template('user-details.html', user=user)

@app.route('/add-user')
def get_user_form():
    """show form to add a user"""
    return render_template("user-form.html")