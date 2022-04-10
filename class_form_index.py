from operator import length_hint
from flask_wtf import FlaskForm  # ซ่อมการทำงาน HTML
from wtforms import TextAreaField, TelField,  BooleanField, SubmitField, SelectField, SearchField, RadioField, FieldList, StringField  # จัดการ HTML
from wtforms.validators import DataRequired


class Myfromindex(FlaskForm):
    # Logout
    Logout = SubmitField("Log Out")


class form_profile(FlaskForm):
    # Logout
    Logout = SubmitField("Log Out")
