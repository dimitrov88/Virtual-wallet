from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, NumberRange
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class CreateTransactionForm(FlaskForm):
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
    amount = StringField("Amount", validators=[DataRequired()])
    submit = SubmitField("Submit Transaction")
