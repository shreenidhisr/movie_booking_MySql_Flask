from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import Required, EqualTo, Email, Length, ValidationError


class signinForm(FlaskForm):
    name = StringField("name", [Required(message="please enter name")])
    email = StringField(
        "email",
        [
            Required(message="please enter email address"),
            Email(message="not a valid email address"),
        ],
    )
    phno = IntegerField("phno", [Required()])
    password = PasswordField(
        "password",
        [Required("must enter password to proceed"), Length(min=8, max=12)],
    )
    # confirm = PasswordField("cofirmpassword", [EqualTo(password)])
    submit = SubmitField("submit")


def my_length_check(form, field):
    if len(field.data) != 10:
        raise ValidationError("mobile number must be of 10 characters")


class loginForm(FlaskForm):
    email = StringField(
        "email",
        [
            Required(message="you must enter email to proceed"),
            Email(message="not a valid email address"),
        ],
    )
    password = PasswordField(
        "password", [Required("must enter password to proceed"), Length(min=8, max=12)]
    )
    submit = SubmitField("submit")
