from operator import length_hint
from flask_wtf import FlaskForm  # ซ่อมการทำงาน HTML
from wtforms import TextAreaField, TelField,  BooleanField, SubmitField, SelectField, SearchField, RadioField, FieldList, StringField  # จัดการ HTML
from wtforms.validators import DataRequired


class MyfromLogin(FlaskForm):
    # Login
    Register_new = SubmitField("Register a new membership")
    forgot_Pass = SubmitField("I forgot my password")
    UserID = TelField(name="UserID")
    User_Password = TelField(name="Password")
    submit = SubmitField("Login")
    Sign_out = SubmitField("Sign out")
    Remember_password = BooleanField(name="Remember password")


class register(FlaskForm):

    Regis_UserID = TelField(name="User ID")
    Regis_UserEmail = TelField(name="Email")
    Regis_User_Password = TelField(
        name="Password")
    Retype_password = TelField(
        name="Retype password")
    Regis_submit_Sign_up = SubmitField("Sign me up")
    already_have = SubmitField("I already have a membership")


class ResetRequestForm(FlaskForm):
    Email = TelField(name="email")
    send_Submit = SubmitField("Send to Email")


class ResetNewPassword(FlaskForm):
    Npassword = TelField(name="Password")
    Confirm_password = TelField(name="Confirm password")
    send_Submit = SubmitField("Chang Password")


class expTOken(FlaskForm):
    send_Submit_toforget = SubmitField("forgot my password")
