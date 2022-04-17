#๒ฟหกฟหกฟหกฟหก
#99999999999999999999
#99999999999999999999
#99999999999999999999
#99999999999999999999
from datetime import timedelta
from distutils.errors import PreprocessError
from operator import truediv
import os
import string
#99999999999999999999
#99999999999999999999
#99999999999999999999
#๒ฟหกฟหกฟหก
from tkinter.tix import Tree
from itsdangerous import TimedSerializer, TimestampSigner
# from distutils.text_file import TextFile
from wsgiref.validate import validator
from flask import Flask, flash, render_template, request, session, redirect, url_for, escape
import flask
from flask_session import Session
from flask_wtf import FlaskForm  # ซ่อมการทำงาน HTML
from flask_mail import Mail, Message

from wtforms import TextAreaField, TelField,  BooleanField, SubmitField, SelectField, SearchField, RadioField  # จัดการ HTML
from wtforms.validators import DataRequired
import mysql.connector
import bcrypt  # เข้าระหัสPASSWORD
import fungtion_Binace
import fu_Mysql
import class_User
import class_form_index
import Bot_spot_1
import mybioneway11
import class_html
#99999999999999999999#99999999999999999999
app = Flask(__name__, static_url_path='/static')
app.config["SECRET_KEY"] = 'mykeysss'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# 60*24 = 1,440 จับเวลา Login 1วัน ให้เคลีย SESSION
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1440)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # 'localhost'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'botteadingview@gmail.com'
app.config['MAIL_PASSWORD'] = 'Z533op/*-'
app.config['MAIL_DEFAULT_SENDER'] = 'botteadingview@gmail.com'

mail = Mail(app)
Session(app)


#############################################################################################################
# เข้าหน้าหลัก ถ้าไม่เจอชื่อ  session["UserID"] == "" ให้ไปหน้า Login
#############################################################################################################


def check_UserID():

    try:

        if session["UserID"] == None or session["UserID"] == '':

            return True
    except:
        print("UserID = error")
        session["UserID"] = ""
        return True


@app.route("/", methods=["POST", "GET"])
def index():

    form = class_form_index.Myfromindex()

    if check_UserID():
        return redirect("/login")

    return render_template('index.html', form=form)

#############################################################################################################
# LOGIN
#############################################################################################################


@app.route("/logout", methods=["GET", "POST"])
def logout():

    session.clear()

    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = class_User.MyfromLogin()
    User_login = form.UserID.data
    Pass_login = form.User_Password.data

    try:
        if session["UserID"]:
            return redirect("/")
    except:
        pass

    if request.method == "POST":

        if User_login != "":
            data = fu_Mysql.User_select_login(User_login, User_login)

            try:
                user_indata = data[0][1]

                try:
                    pass_indata = data[0][3]

                    if bcrypt.checkpw(bytes(Pass_login, 'utf-8'), bytes(pass_indata, 'utf-8')) and User_login == user_indata:

                        print("OK")
                        # ตัวเช็ก การเข้าใช้อยู่มั้ย
                        session["UserID"] = form.UserID.data
                        session.permanent = True

                        session["is_math_Password"] = ""
                        return redirect("/")
                    else:
                        Pass_login = "donmatch"

                except:
                    Pass_login = "donmatch"
                    print("Password ไม่ถูกต้อง")
            except:
                User_login = "UserIDincorrect"
                print("ไม่พบ ชื่อผู้ใช้นี้ "+User_login+request.method)
        else:
            User_login = ""
    if form.Register_new.data:
        return redirect("/register")

    return render_template("login.html", form=form, name=User_login, passlogin=Pass_login)


@app.route("/Dashboard", methods=["GET", "POST"])
def Dashboard():

    form = class_form_index.form_Dashboard()
    if check_UserID():
        return redirect("/login")

    session['playlist_id'] = ""
    u_id = session["UserID"]

    data = fu_Mysql.API_select(u_id, "")
    data_alert = fu_Mysql.Alert_select(u_id, '', '', '', '')
    htmls = ""
    html_m = ""

    session["ch_api"] = ""
    delete = form.delete.data
    pause = form.pause.data
    api_update = form.api_update.data
    Create_API = form.Create_API.data
    pass_action = form.pass_action.data

    if request.method == "POST":

        if pause:
            if pass_action.split("_")[0] == "pause":
                id_ = pass_action.replace("pause_bot_", "")
                fu_Mysql.API_PauseOrRun(id_, "run")
            else:
                id_ = pass_action.replace("running_bot_", "")
                fu_Mysql.API_PauseOrRun(id_, "stop")
            return redirect("/Dashboard")

        if delete:
            id_ = pass_action.replace("delete_bot_", "")
            fu_Mysql.API_Delete(id_)
            return redirect("/Dashboard")

        if api_update:
            id = pass_action.replace("detail_Bot_", "")
            Label_API = form.set_txt1.data
            API_Key = form.set_txt2.data
            API_SECRET = form.set_txt3.data
            LineNotify = form.set_txt4.data
            PassPhrase = form.set_txt5.data
            MarginType = form.set_txt6.data
            ReOpenOrder = form.set_txt7.data

            fu_Mysql.API_Update(id, Label_API, API_Key, API_SECRET, LineNotify,
                                PassPhrase, MarginType, ReOpenOrder)
            return redirect("/Dashboard")

        if Create_API:

            bot_type = form.to0X8sp765598as00zo23.data
            Label_API = form.Label_API.data
            API_Key = form.API_Key.data
            API_SECRET = form.API_SECRET.data
            LineNotify = form.LineNotify.data
            PassPhrase = form.PassPhrase.data
            MarginType = form.MarginType.data
            ReOpenOrder = form.ReOpenOrder.data

            check_apikey = fu_Mysql.API_select("", API_Key)
            if check_apikey != []:
                session["ch_api"] = "have"
                print(session["ch_api"])
            else:

                fu_Mysql.API_insert(u_id, API_Key, API_SECRET, LineNotify, PassPhrase,
                                    MarginType, ReOpenOrder, "", Label_API, bot_type, "stop")
                return redirect("/Dashboard")

    if data_alert != []:
        html_Alert = ""
        for x in data_alert:

            html_Alert += class_html.html_alert(
                x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9])
            print(html_Alert)
            session["html_Alert"] = html_Alert
    else:
        session["html_Alert"] = ""
    if data != []:

        for x in data:

            htmls += class_html.html_isbot(x[0], x[11], x[9], x[10], x[12])
            html_m += class_html.html_modal(
                x[0], x[11], x[6], x[7], x[10], x[2], x[3], x[4], x[5])
            session["html_isbot"] = htmls
            session["html_modal"] = html_m

    else:
        session["html_modal"] = ""
        session["html_isbot"] = ""
        print("data : non")

    return render_template("Dashboard.html", form=form)


@app.route("/singup", methods=["GET", "POST"])
def singup():

    form = class_User.register()
    User_login = form.Regis_UserID.data
    email = form.Regis_UserEmail.data
    Pass_login = form.Regis_User_Password.data
    Retypepass = form.Retype_password.data
    countPass = 0

    if request.method == "POST":
        data = fu_Mysql.User_select_login("nateeron", "")
        user_indata = data[0][1]
        email_data = data[0][2]
        print(type(email))
        print(Pass_login)

        print(Pass_login)
        if Pass_login:  # != "" and Pass_login != None:
            countPass = len(Pass_login)

            if countPass < 5:
                Pass_login = "len5"
        if Pass_login == Retypepass:
            hashed_Str = ""
            if User_login and email and Pass_login and Retypepass:
                # if request.method == "POST":
                hashed = bcrypt.hashpw(
                    Pass_login.encode("utf-8"), bcrypt.gensalt())
                hashed_Str = hashed.decode("utf-8")
                if user_indata == User_login:
                    User_login = "user_already"
                    print("********* This username already exists. ********")
                    render_template("signup.html", form=form, name=User_login,
                                    email=email, passlogin=Pass_login, Retype_password=Retypepass)
                elif email_data == email:
                    email = "Email_already"
                    print("********* This Email already exists. ********")
                    render_template("signup.html", form=form, name=User_login,
                                    email=email, passlogin=Pass_login, Retype_password=Retypepass)
                else:
                    fu_Mysql.User_create(User_login, email, hashed_Str)
                    print("*********OK*********")
                    return redirect("/login")
        else:
            if Pass_login != "len5":
                Retypepass = "dontmatch"

    print(Retypepass)
    return render_template("signup.html", form=form, name=User_login, email=email, passlogin=Pass_login, Retype_password=Retypepass)
#############################################################################################################
# Register
#############################################################################################################


@app.route("/register", methods=["GET", "POST"])
def register():
    form = class_User.register()
    if request.method == "POST":
        session["Regis_UserEmail"] = form.Regis_UserEmail.data
        session["Regis_UserID"] = form.Regis_UserID.data
        session["Regis_User_Password"] = form.Regis_User_Password.data

        if form.Regis_UserEmail.data and form.Regis_UserID.data and form.Regis_User_Password.data:
            session["UserID"] = form.Regis_UserID.data
            return redirect("/")

    return render_template("login.html", form=form)


#############################################################################################################
# Reset Password
#############################################################################################################
def auth_token(user):
    return os.urandom(12).encode('hex') + app.config["SECRET_KEY"](user['email'] + user['pwd_hash'])


def password_reset_token(user):
    signer = TimestampSigner(app.config["SECRET_KEY"])

    return signer.sign(str(user))


def validate_password_reset_token(token):
    signer = TimestampSigner(app.config["SECRET_KEY"])

    return signer.unsign(token, max_age=1000)  # 300 = 5 นาที


print("**********************************************************************")


@app.route("/test", methods=["GET", "POST"])
def test():
    form = class_User.ResetNewPassword()
    return render_template("send_resetPass.html", form=form)


##################[ Send Mail ]###############
def send_mail(Email_user):
    token = password_reset_token(Email_user)

    print("1..token.<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print([app.config['MAIL_USERNAME']])
    print([Email_user])

    with app.app_context():
        msg = Message(subject='Password Reset Request',
                      recipients=['nateeronron@gmail.com'], sender='botteadingview@gmail.com')
        msg.body = f''' To Reset You password. Please follow the link below.

                    {url_for('reset_new_password',token=token,_external = True)}
                    
                    If you didn't send a Password reset request.

                    '''
        msg.html = '<a href="http://192.168.43.94:5000/reset_new_password/' + \
            token.decode("utf-8")+'">Reset You password</a>'

        mail.send(msg)

    return "send_success"


@ app.route("/resetpass", methods=["GET", "POST"])
def resetpass():
    form = class_User.ResetRequestForm()
    session["mail_in"] = form.Email.data
    send_success = ""
    if request.method == "POST":
        print("session[mail_in]")
        print(session["mail_in"])
        # ดุงข้อมูลจาก DATA  nateeron9@gmail.com
        try:
            data = fu_Mysql.User_select_login("", session["mail_in"])

            if data != {}:
                Email_fromDATA = data[0][2]

                if Email_fromDATA:
                    # ใช้ชื่อที่ได้จากDATA ค้นหาด้วย Email
                    # sender='botteadingview@gmail.com',, body="aaaaaaaaaaaaaaaaaaaaaaaaaaa"+
                    send_success = send_mail(Email_fromDATA)
                    return render_template("reset_Pass.html", form=form, notfound=send_success)
                # redirect("/login")
            else:
                send_success = "notfound"
                return print("ไม่พบผู้ใช้")
        except:

            send_success = "notfound"
            return render_template("reset_Pass.html", form=form, notfound=send_success)
    return render_template("reset_Pass.html", form=form, notfound=send_success)


################[ reset_new_password ]#####################
@ app.route("/reset_new_password/<token>", methods=["GET", "POST"])
def reset_new_password(token):
    form = class_User.ResetNewPassword()
    check = ""
    try:
        chacks = validate_password_reset_token(token)
        print(chacks)
        # ถ้า token ไม่หมดอายุให้ รอเปลี่ยน Pass
        print(request.method)

        if request.method == "POST":
            pass_Chang = str(form.Npassword.data)
            newPass = str(form.Confirm_password.data)
            if newPass == pass_Chang:
                newPass = str(form.Confirm_password.data)
                # เวลาเซฟ
                hashed = bcrypt.hashpw(
                    newPass.encode("utf-8"), bcrypt.gensalt())
                hashed_Str = (hashed).decode("utf-8")
                email = str(chacks.decode("utf-8"))
                fu_Mysql.User_Update("", email,  "", "", hashed_Str)
                return render_template("reset_new_password.html", form=form, check_password=check)
            else:
                check = "dontmatch"
    except:
        print("Token หมดอายุ")
        return redirect("/Tokens_expire")

    return render_template("reset_new_password.html", form=form, check_password=check)


@ app.route("/Tokens_expire", methods=["GET", "POST"])
def Tokens_expire():
    form = class_User.expTOken()
    if request.method == "POST":

        return redirect("/resetpass")
    return render_template("Tokens_expire.html", form=form)


@app.route("/profile", methods=["GET", "POST"])
def profile():

    if check_UserID():  # session["UserID"] == None or session["UserID"] == '':

        return redirect("/login")
    form = class_form_index.form_profile()

    return render_template("pages-profile.html", form=form)


# --------------Bot Spot---------------------------@@@@@@@@@@@@@@@@@@@@@@@@@@@-------------------------------------


@app.route("/Cayoshibot", methods=["POST"])
def Cayoshibot():
    if request.method == "POST":
        Bot_spot_1.CayoshiM()

    return ""


@app.route('/mybotnaja', methods=['POST', 'GET'])
def mybotnaja():
    if request.method == "POST":
        mybioneway11.mywebhook()
    return ""


@app.route('/status')
def status():
    webmessage = "on"
    return webmessage


@app.errorhandler(404)
def page_not_dound(e):
    session['404'] = e
    return render_template("404.html")


if __name__ == '__main__':

    app.run(debug=True, host="0.0.0.0",  port=5000)
