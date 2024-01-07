from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from datetime import datetime
from forms import RegisterForm, LoginForm, CommentForm, AddFromCardForm, CreateTransactionForm, ContactForm, CreateFriendTransactionForm
from werkzeug.security import generate_password_hash, check_password_hash
from data.models import BaseUser, Wallet, TransactionResponse, WalletResponse
from services import user_services, wallet_services, transaction_services
from flask import request

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
    return user_services.get_by_id(user_id)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    # posts = get_posts()
    form = LoginForm()
    return render_template("login.html", form=form)


@app.route('/home')
def home():
    user_wallet = wallet_services.get_by_user_name(current_user.name)
    user_transactions = transaction_services.get_by_username(current_user.name)

    return render_template("index1.html", current_user=current_user, wallet=user_wallet, transactions=user_transactions)


@app.route("/add_money/<int:current_wallet_id>", methods=["GET", "POST"])
def add_money(current_wallet_id: int):
    form = AddFromCardForm()
    if form.validate_on_submit():
        amount = form.amount.data
        wallet = wallet_services.get_by_id(current_wallet_id)
        to_add = wallet_services.add_from_card(wallet, float(amount))

        flash("Money added successfully!")
        return redirect(url_for("home"))
    return render_template("add_from_card.html", form=form)


@app.route("/create_transaction/<int:current_wallet_id>", methods=["GET", "POST"])
def create_transaction(current_wallet_id: int):
    form = CreateTransactionForm()
    if form.validate_on_submit():
        sender_wallet = wallet_services.get_by_id(current_wallet_id)

        receiver_wallet = wallet_services.get_by_email(form.receiver.data)
        amount = float(form.amount.data)
        if sender_wallet.balance < amount:
            flash("You do not have enough money.")
            return redirect(url_for("create_transaction"))
        to_send = wallet_services.make_transaction(sender_wallet, receiver_wallet, amount)
        flash("Transaction complete!")
        return redirect(url_for("home"))
    return render_template("make_transaction.html", form=form)


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


@app.route("/my_contacts")
def my_contacts():
    all_contacts = user_services.get_all_contacts_by_id(current_user.id)
    return render_template("contacts.html", current_user=current_user, contacts=all_contacts)


@app.route("/add_contact", methods=["GET", "POST"])
def add_contact():
    form = ContactForm()

    if form.validate_on_submit():
        check_user = user_services.get_by_email(form.email.data)
        if not check_user:
            flash("User with that email doesn't exist!")
            return render_template("contact_form.html", current_user=current_user, form=form)
        else:
            to_add = user_services.add_contact(current_user.id, check_user.id)
            flash("Contact added successfully!")
            return redirect(url_for("my_contacts"))
    return render_template("contact_form.html", form=form)


@app.route("/remove_contact/<int:contact_id>")
def remove_contact(contact_id: int):
    to_remove = user_services.remove_contact_by_id(contact_id, current_user.id)
    flash("Contact removed!")
    return redirect(url_for("my_contacts"))


@app.route("/send_to_friend/<int:contact_id>",  methods=["GET", "POST"])
def send_to_friend(contact_id: int):
    form = CreateFriendTransactionForm()
    friend = user_services.get_by_id(contact_id)
    if form.validate_on_submit():
        sender_wallet = wallet_services.get_by_user_id(current_user.id)

        receiver_wallet = wallet_services.get_by_email(friend.email)
        amount = float(form.amount.data)
        if sender_wallet.balance < amount:
            flash("You do not have enough money.")
            return redirect(url_for("send_to_friend"))
        to_send = wallet_services.make_transaction(sender_wallet, receiver_wallet, amount)
        flash("Transaction complete!")
        return redirect(url_for("home"))
    return render_template("send_to_friend.html", form=form, contact=friend)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        # Check if user email is already present in the database.
        user = user_services.get_by_email(form.email)

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

        insert_user = user_services.create_user(new_user)
        first_wallet = (wallet_services.create_first_wallet
                        (Wallet(name=f"{new_user.name} EUR Wallet", balance=0), new_user.name))
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
        user = user_services.get_by_email(form.email.data)

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
            return redirect(url_for('home'))  # TODO switch url

    return render_template("login.html", form=form, current_user=current_user)


if __name__ == "__main__":
    app.run(debug=True, port=5002)
