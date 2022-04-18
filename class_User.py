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


class Profile(FlaskForm):
    Save_Changes = SubmitField("Save Changes")
    UserID = TelField(name="UserID Name")
    User_Password = TelField(name="Password")
    User_NewPassword = TelField(name="New Password")
    UserEmail = TelField(name="Email")
    exchange = SelectField("exchange", choices=[
        ("Binace", "Binace"), ("Bitkub", "Bitkub")])
    spot_future = SelectField("spot_future", choices=[
                              ("Spot", "Spot"), ("Future", "Future")])
    buy_demo = SubmitField("Demo 1 Month")
    buy_1 = SubmitField("Buy 1 Month")
    buy_3 = SubmitField("Buy 3 Month")
    buy_12 = SubmitField("Buy 12 Month")


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
