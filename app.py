"""Blogly application."""

from flask import Flask, render_template
from models import db, connect_db
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)


app.config['SECRET_KEY'] = "mysecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def get_home():
    return render_template('home.html')