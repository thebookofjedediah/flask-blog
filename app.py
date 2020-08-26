from flask import Flask, render_template, redirect, request
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
def get_home():
    """shows list of all users"""
    return redirect('/users')

@app.route('/users')
def get_users():
    """shows list of all users"""
    users = User.query.all()
    return render_template('list.html', users=users)

@app.route('/users/<int:user_id>')
def user_details(user_id):
    """show details about user"""
    user = User.query.get(user_id)
    return render_template('user-details.html', user=user)

@app.route('/users/new')
def get_user_form():
    """show form to add a user"""
    return render_template("user-form.html")

@app.route('/users', methods=["POST"])
def create_user():
    """add a user with the form data"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url or None)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Handle form submission for deleting an existing user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/edit')
def user_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user-edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]
 
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

