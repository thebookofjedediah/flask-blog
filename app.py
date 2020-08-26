from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post
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
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('home.html', posts=posts)

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

# PART TWO
@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    """form for creating a new post"""
    user = User.query.get_or_404(user_id)
    return render_template('new-post.html', user=user)

# @app.route('/users/<int:user_id>/posts/new', methods=["POST"])
# def add_post(user_id):
#     """Create new post"""
#     user = User.query.get_or_404(user_id)
#     new_post = Post(title = request.form["title"], content = request.form["content"], user=user)

#     db.session.add(new_post)
#     db.session.commit()

#     return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """Show a page with info on a specific post"""

    post = Post.query.get_or_404(post_id)
    return render_template('post-details.html', post=post)


@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """Show a form to create a new post for a specific user"""

    user = User.query.get_or_404(user_id)
    return render_template('new-post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """Handle form submission for creating a new post for a specific user"""

    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>/edit')
def post_edit(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post-edit.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission for editing an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
 
    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handle form submission for deleting an existing post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect("/users")