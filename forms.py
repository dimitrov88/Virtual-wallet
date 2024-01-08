from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, URL, NumberRange
from flask_ckeditor import CKEditorField
from flask_login import current_user
from services import wallet_services


# class CreateTransactionForm(FlaskForm):
#     wallet = SelectField("Select wallet (Optional)", choices=[("", "Select Wallet")])
#     receiver = StringField("Receiver email", validators=[DataRequired()])
#     amount = StringField("Amount", validators=[DataRequired()])
#     submit = SubmitField("Submit Transaction")

def wallet_choices():
    data = [("", "Select Wallet")]
    all_user_wallets = wallet_services.get_all_wallets(current_user.id)
    to_add = [(w.name, f"{w.name}") for w in all_user_wallets]
    data.extend(to_add)

    return data


class CreateTransactionForm(FlaskForm):
    wallet = SelectField("Select wallet (Optional)", choices=wallet_choices)
    receiver = StringField("Receiver email", validators=[DataRequired()])
    amount = StringField("Amount", validators=[DataRequired()])
    submit = SubmitField("Submit Transaction")


# Create a form to register new users
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


# Create a form to login existing users
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")


# Create a form to add comments
class CommentForm(FlaskForm):
    comment_text = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")


class AddFromCardForm(FlaskForm):
    card_number = StringField("Card number", validators=[DataRequired()])
    card_holder = StringField("Card holder", validators=[DataRequired()])
    amount = StringField("Amount to send", validators=[DataRequired()])
    submit = SubmitField("Add money")


class ContactForm(FlaskForm):
    email = StringField("Friend's email", validators=[DataRequired()])
    submit = SubmitField("Add contact!")


class CreateFriendTransactionForm(FlaskForm):
    wallet = SelectField("Select wallet (Optional)", choices=wallet_choices)
    amount = StringField("Amount", validators=[DataRequired()])
    submit = SubmitField("Submit Transaction")
