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


class form_Dashboard(FlaskForm):
    Logout = SubmitField("Log Out")
    Create_API = SubmitField("Create API")

    Label_API = TelField("Label API")
    API_Key = TelField(name="API Key")
    API_SECRET = TelField(name="API SECRET")
    LineNotify = TelField(name="LineNotify")
    PassPhrase = TelField(name="Pass Phrase")
    MarginType = RadioField(
        choices=[('ISOLATED', 'ISOLATED'), ('CROSSED', 'CROSSED')])
    ReOpenOrder = RadioField(choices=[('ON', 'ON'), ('OFF', 'OFF')])
    to0X8sp765598as00zo23 = StringField("to0X8sp765598as00zo23")
    delete = SubmitField("Delete")

    pause = SubmitField("Yes")
    pass_action = TelField(name="pass_action")
    api_update = SubmitField("UPDATE")

    set_txt1 = TelField("set_txt1")
    set_txt2 = TelField("set_txt2")
    set_txt3 = TelField("set_txt3")
    set_txt4 = TelField("set_txt4")
    set_txt5 = TelField("set_txt5")
    set_txt6 = TelField("set_txt6")
    set_txt7 = TelField("set_txt7")

    test_send = SubmitField("TEST SEND")
    send_post = TelField("send post")
