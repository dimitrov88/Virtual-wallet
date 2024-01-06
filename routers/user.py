from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm, CommentForm
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from main import app, login_manager
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from services.user_services import get_by_id, get_by_email, create_user
from services.wallet_services import create_first_wallet
from data.models import BaseUser, Wallet


@login_manager.user_loader
def load_user(user_id):
    return get_by_id(user_id)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


# Register new users into the User database

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
        first_wallet = create_first_wallet(Wallet(name=f"{new_user.name} EUR Wallet", currency="EUR"), new_user.name)

        # This line will authenticate the user with Flask-Login
        login_user(new_user)
        return redirect(url_for("login"))
    return render_template("register.html", form=form, current_user=current_user)


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
