

import os
import string
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

app = Flask(__name__, static_url_path='/static')
app.config["SECRET_KEY"] = 'mykeysss'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

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


@app.route("/", methods=["POST", "GET"])
def index():

    form = class_form_index.Myfromindex()

    if session["UserID"] == None or session["UserID"] == '':

        return redirect("/login")

    if request.method == "POST" and session["UserID"] != '':

        logout = form.Logout.check_validators()
        print(logout)
        print(request.method)
    return render_template('index.html', form=form)

#############################################################################################################
# LOGIN
#############################################################################################################


@app.route("/logout", methods=["GET", "POST"])
def logout():

    session["UserID"] = ""

    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = class_User.MyfromLogin()

    # if request.method == "POST":
    User_login = form.UserID.data
    Pass_login = form.User_Password.data
    print(form.UserID.data)
    if session["UserID"]:
        return redirect("/")
    if request.method == "POST":
        print("USREID//////////////////////////////////////////////////")
        print(User_login)
        if User_login != "":
            data = fu_Mysql.User_select_login(User_login, User_login)
            print("print(data)")
            print(data)
            try:
                user_indata = data[0][1]
                print(Pass_login)
                try:
                    pass_indata = data[0][3]

                    if bcrypt.checkpw(bytes(Pass_login, 'utf-8'), bytes(pass_indata, 'utf-8')) and User_login == user_indata:

                        print("OK")
                        # ตัวเช็ก การเข้าใช้อยู่มั้ย
                        session["UserID"] = form.UserID.data
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


@app.route("/singup", methods=["GET", "POST"])
def singup():

    form = class_User.register()
    User_login = form.Regis_UserID.data
    email = form.Regis_UserEmail.data
    Pass_login = form.Regis_User_Password.data
    Retypepass = form.Retype_password.data
    countPass = 0
    print(countPass)
    print(Retypepass)
    if request.method == "POST":
        if Pass_login != "" and Pass_login != None:
            countPass = len(Pass_login)

            if countPass < 5:
                Pass_login = "len5"
        if Pass_login == Retypepass:
            hashed_Str = ""
            if User_login != "" and email != "" and Pass_login != "" and Retypepass != "":
                # if request.method == "POST":
                hashed = bcrypt.hashpw(
                    Pass_login.encode("utf-8"), bcrypt.gensalt())
                hashed_Str = hashed.decode("utf-8")

                fu_Mysql.User_create(User_login, email, hashed_Str)
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

    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # con = fu_Mysql.User_create("admin7", "nateeron8@gmail.com",
    # "$2b$12$UrTBoRa1FlV5XWZVyHZUnO6M5myLdT.KBCJXgVYy2cnEE87k6/mka")
    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    return render_template("send_resetPass.html", form=form)

    # return redirect(url_for('reset_new_password'))
##################[ Send Mail ]###############


def send_mail(Email_user):
    token = password_reset_token(Email_user)

    print("1..token.<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print([app.config['MAIL_USERNAME']])
    print([Email_user])

    #html = forms.Html_send_resetPassword(token)
    # print(html)
    with app.app_context():
        msg = Message(subject='Password Reset Request',
                      recipients=['nateeronron@gmail.com'], sender='botteadingview@gmail.com')
        msg.body = f''' To Reset You password. Please follow the link below.

                    {url_for('reset_new_password',token=token,_external = True)}
                    
                    If you didn't send a Password reset request.

                    '''
        msg.html = '<a href="http://192.168.43.94:5000/reset_new_password/' + \
            token.decode("utf-8")+'">Reset You password</a>'
        # msg.html = (
        # u'<a href="{{url_for(''reset_new_password'')}}">abc</a>', 'html')
        mail.send(msg)

#_external = True
    return "send_success"
#############################################
# # type="submit"


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

                print("********** 1 **************")
                newPass = str(form.Confirm_password.data)
                print("********** 2 **************")
                # เวลาเซฟ
                hashed = bcrypt.hashpw(
                    newPass.encode("utf-8"), bcrypt.gensalt())
                print("********** 3 **************")
                hashed_Str = (hashed).decode("utf-8")
                print("********** 4 **************")
                print(str(chacks.decode("utf-8")))
                email = str(chacks.decode("utf-8"))

                fu_Mysql.User_Update("", email,  "", "", hashed_Str)

                #flash('Password chang! Please Login', 'success')
                print("********** 5 **************")
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
    form = class_form_index.form_profile()

    return render_template("pages-profile.html", form=form)


################################################################################################################################################################################################################################################
################################################################################################################################################################################################################################################


@ app.route('/pass')
def hello_world():
    passwordb = b"Pass1234"
    password = "Pass1234"
    # เวลาเซฟ
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    # username = request.form.get("username") # or email
    # passwords = request.form.get(password).encode("utf-8")
    passwords = (password).encode("utf-8")
    # เช็กระหัส
    print(passwords)
    print(hashed)
    if bcrypt.checkpw(passwords, hashed):
        # return "<h1>ChackPass</h1><br><h2>Wellcom"+password+"</h2>"
        print(fungtion_Binace.cal_1())
        return "<h1>ChackPass</h1><br><h2>Wellcom "+fungtion_Binace.cal_1()+"</h2>"

    else:

        return "<h1>ChackPass</h1><br><h2>Didn't match Pass </h2>"


@ app.route('/admin')
def admin():
    return "Admin"

# --------------Bot Spot---------------------------@@@@@@@@@@@@@@@@@@@@@@@@@@@-------------------------------------


@app.route("/Cayoshibot", methods=["POST"])
def Cayoshibot():
    if request.method == "POST":
        Bot_spot_1.CayoshiM()

    return ""


if __name__ == '__main__':

    app.run(debug=True, host="0.0.0.0",  port=5000)
