from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from datetime import datetime
from forms import RegisterForm, LoginForm, CommentForm, AddFromCardForm
from services.user_services import get_by_id, get_by_email
from werkzeug.security import generate_password_hash, check_password_hash
from data.models import BaseUser, Wallet
from services.user_services import create_user
from services.wallet_services import create_first_wallet

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return get_by_id(user_id)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    # posts = get_posts()
    return render_template("index1.html", current_user=current_user)


@app.route("/add_money")
def add_money():
    form = AddFromCardForm()
    if form.validate_on_submit():
        amount = form.amount.data


    return render_template("add_from_card.html")


# @app.route('/')
# def get_all_posts():
#     # posts = get_posts()
#     return render_template("index1.html", all_posts=posts, current_user=current_user)

# # Add a POST method to be able to post comments
# @app.route("/post/<int:post_id>", methods=["GET", "POST"])
# def show_post(post_id):
#     requested_post = get_post_by_id(post_id)
#     # Add the CommentForm to the route
#     comment_form = CommentForm()
#     # Only allow logged-in users to comment on posts
#     if comment_form.validate_on_submit():
#         if not current_user.is_authenticated:
#             flash("You need to login or register to comment.")
#             return redirect(url_for("login"))
#
#         new_comment = Comments(
#             text=comment_form.comment_text.data,
#             author=current_user.name
#         )
#         result = add_comment(new_comment.text, current_user, requested_post.id)
#         if result:
#             requested_post.comments.append(result)
#
#     return render_template("post.html", post=requested_post, current_user=current_user, form=comment_form)
#
#
# # Use a decorator so only an admin user can create new posts
# @app.route("/new-post", methods=["GET", "POST"])
# def add_new_post():
#     form = CreatePostForm()
#     if form.validate_on_submit():
#         new_post = BlogPost(
#             title=form.title.data,
#             subtitle=form.subtitle.data,
#             body=form.body.data,
#             img_url=form.img_url.data,
#             date=datetime.now(),
#             author=current_user.name
#         )
#         insert = add_post(new_post, current_user)
#
#         return redirect(url_for("get_all_posts"))
#     return render_template("make-post.html", form=form, current_user=current_user)
#
#
# # Use a decorator so only an admin user can edit a post
# @app.patch("/edit-post/<int:post_id>")
# def edit_post(post_id):
#     post = get_post_by_id(post_id)
#     edit_form = CreatePostForm(
#         title=post.title,
#         subtitle=post.subtitle,
#         img_url=post.img_url,
#         author=current_user.name,
#         body=post.body
#     )
#     if edit_form.validate_on_submit():
#         post.title = edit_form.title.data
#         post.subtitle = edit_form.subtitle.data
#         post.img_url = edit_form.img_url.data
#         post.author = current_user.name
#         post.body = edit_form.body.data
#
#         result = update_post(post)
#
#         return redirect(url_for("show_post", post_id=post.id))
#     return render_template("make-post.html", form=edit_form, is_edit=True, current_user=current_user)
#
#
# @app.route("/delete/<int:post_id>", methods=["GET", "POST", "DELETE"])
# def delete_post(post_id):
#     if not current_user.is_authenticated:
#         flash("You need to login.")
#         return redirect(url_for("login"))
#
#     post_to_delete = get_post_by_id(post_id)
#     if not post_to_delete:
#         flash("Post Do Not Exist!")
#         return redirect(url_for("get_all_posts"))
#
#     if post_to_delete.author != current_user.name:
#         return redirect(url_for("get_all_posts"))
#
#     result = remove_post(post_id)
#
#     return redirect(url_for('get_all_posts'))
#
#
# @app.route("/delete/comment/<int:comment_id>", methods=["GET", "POST", "DELETE"])
# def delete_comment(comment_id):
#     to_delete = get_comment_by_id(comment_id)
#     if to_delete.author == current_user.name:
#         action = remove_comment(comment_id)
#
#     return redirect(url_for('get_all_posts'))
#
#
@app.route("/about")
def about():
    return render_template("about.html", current_user=current_user)


@app.route("/contact")
def contact():
    return render_template("contact.html", current_user=current_user)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        # Check if user email is already present in the database.
        user = get_by_email(form.email)

        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = BaseUser(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password
        )

        insert_user = create_user(new_user)
        first_wallet = create_first_wallet(Wallet(name="EUR Wallet", currency="EUR"), new_user.name)

        # This line will authenticate the user with Flask-Login
        login_user(new_user)
        return redirect(url_for("login"))
    return render_template("register.html", form=form, current_user=current_user)


#
#
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        user = get_by_id(form.email.data)

        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('get_all_posts'))  # TODO switch url

    return render_template("login.html", form=form, current_user=current_user)


if __name__ == "__main__":
    app.run(debug=True, port=5002)
