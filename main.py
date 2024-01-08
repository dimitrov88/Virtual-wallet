from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import LoginManager, current_user, logout_user
from routers import transaction, user
from forms import LoginForm, AddFromCardForm
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

app.register_blueprint(transaction.transaction_bp)
app.register_blueprint(transaction.friend_transaction_bp)
app.register_blueprint(user.register_bp)
app.register_blueprint(user.login_bp)
app.register_blueprint(user.my_contacts_bp)
app.register_blueprint(user.add_contact_bp)
app.register_blueprint(user.remove_contact_bp)
app.register_blueprint(transaction.add_money_bp)
app.register_blueprint(user.logout_bp)
app.register_blueprint(transaction.home_bp)
app.register_blueprint(transaction.home_amount_bp)


@login_manager.user_loader
def load_user(user_id):
    return user_services.get_by_id(user_id)


@app.route('/')
def wellcome_page():
    form = LoginForm()

    return render_template("wellcome_page.html", form=form)


@app.route("/about")
def about():
    return render_template("about.html", current_user=current_user)


@app.route("/contact")
def contact():
    return render_template("contact.html", current_user=current_user)


if __name__ == "__main__":
    app.run(debug=True, port=5002)
