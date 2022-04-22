

from datetime import timedelta
from distutils.errors import PreprocessError
from operator import truediv
import os
import string
from time import process_time_ns
from datetime import datetime, date
from tkinter.tix import Tree
from itsdangerous import TimedSerializer, TimestampSigner
# from distutils.text_file import TextFile
from wsgiref.validate import validator
from flask import Flask, flash, render_template, request, session, redirect, url_for, escape, jsonify
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
#import Bot_spot_1
import Bot_Spot
import func_futures
import class_html
import socket
import sys
import uuid
import json
from pprint import pprint
import cgi

from subprocess import Popen, PIPE
import re

form = cgi.FieldStorage()
searchterm = form.getvalue('searchbox')
#app = Flask(__name__, static_url_path='/static')
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

        session["UserID"] = ""
        return True


@app.route("/", methods=["POST", "GET"])
def index():

    if check_UserID():
        return redirect("/login")

    return redirect("/Dashboard")

#############################################################################################################
# LOGIN
#############################################################################################################


@app.route("/logout", methods=["GET", "POST"])
def logout():

    session.clear()

    return redirect("/login")


@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    hostname = socket.gethostname()

    IP = request.remote_addr
    stri = IP+' <br> '+' \n 192.168.43.94'
    return stri


@app.route("/login", methods=["GET", "POST"])
def login():

    form = class_User.MyfromLogin()
    User_login = form.UserID.data
    Pass_login = form.User_Password.data

    hostname = socket.gethostname()
    #ip = socket.gethostbyname(hostname)
    ip = request.remote_addr
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

                        # ตัวเช็ก การเข้าใช้อยู่มั้ย
                        session["UserID"] = form.UserID.data
                        fu_Mysql.User_Login_IP(User_login, ip, hostname)
                        session.permanent = True

                        session["is_math_Password"] = ""
                        return redirect("/")
                    else:
                        Pass_login = "donmatch"

                except:
                    Pass_login = "donmatch"

            except:
                User_login = "UserIDincorrect"

        else:
            User_login = ""
    if form.Register_new.data:
        return redirect("/register")

    return render_template("login.html", form=form, name=User_login, passlogin=Pass_login)


@app.route("/about", methods=["GET"])
def about():

    return render_template("about.html")


@app.route("/Dashboards/<string:info>", methods=["GET"])
def Dashboards(info):
    print('*****************[info]************************')
    print(info)
    u_id = session["UserID"]
    data_User = fu_Mysql.User_select_Promo(u_id)
    date_ex = ""
    botdata_type = ""
    if data_User != []:
        try:
            bot_type = info

            for data in data_User:
                try:
                    date_ex = data[6]
                    botdata_type = data[4]
                except:
                    session["ch_Promotion"] = 'isBuy'
                ExpirationDate = datetime.strptime(date_ex, "%Y-%m-%d").date()
                now = date.today()
                if ExpirationDate >= now and bot_type == botdata_type:
                    session["ch_Promotion"] = 'OK'
                    Label_API = request.form['Label_API']
                    API_Key = request.form['API_Key']
                    API_SECRET = request.form['API_SECRET']
                    LineNotify = request.form['LineNotify']
                    MarginType = request.form['MarginType']
                    ReOpenOrder = request.form['ReOpenOrder']
                    uuids = str(uuid.uuid4())
                    PassPhrase = uuid.uuid5(
                        uuid.NAMESPACE_DNS, session["UserID"]+bot_type+uuid)
                    fu_Mysql.API_insert(u_id, API_Key, API_SECRET, LineNotify, PassPhrase,
                                        MarginType, ReOpenOrder, "", Label_API, bot_type, "stop")
                    return redirect("/Dashboard")

                else:
                    session["ch_Promotion"] = 'isBuy'
                    return redirect("/Dashboard")
        except:
            session["ch_Promotion"] = 'isBuy'
            return redirect("/Dashboard")

    return ""  # redirect("/Dashboard")


def count_page(u_id):

    cpunt_data = fu_Mysql.User_select_login(u_id, '')[0][5]

    if cpunt_data != '' and cpunt_data != None:
        count = int(cpunt_data) + 1
        fu_Mysql.User_Count_Page(u_id,  str(count))
    else:
        count = 1
        fu_Mysql.User_Count_Page(u_id,  str(count))


@app.route("/Dashboard", methods=["GET", "POST"])
def Dashboard():
    print('*****************[info 888]************************')

    form_dashb = class_form_index.form_Dashboard()
    if check_UserID():
        return redirect("/login")
    u_id = session["UserID"]
    count_page(u_id)
    data = fu_Mysql.API_select(u_id, "", "")
    data_alert = fu_Mysql.Alert_select(u_id, '', '', '', '')
    session["ch_api"] = ""
    delete = form_dashb.delete.data
    pause = form_dashb.pause.data
    Create_API = form_dashb.Create_API.data
    pass_action = form_dashb.pass_action.data
    send_post = form_dashb.send_post.data
    bot_type = form_dashb.to0X8sp765598as00zo23.data

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

        if request.form.get('test_send') == "TEST SEND":
            print(type(send_post))
            req_data = json.loads(send_post)
            func_futures.bin_func._binanceOneway(req_data)
            Bot_Spot.CayoshiM(send_post)
            return redirect("/Dashboard")
        if request.form.get('api_update') == "API UPDATE":

            id = pass_action.replace("detail_Bot_", "")
            Label_API = form_dashb.set_txt1.data
            API_Key = form_dashb.set_txt2.data
            API_SECRET = form_dashb.set_txt3.data
            LineNotify = form_dashb.set_txt4.data
            PassPhrase = form_dashb.set_txt5.data
            MarginType = form_dashb.set_txt6.data
            ReOpenOrder = form_dashb.set_txt7.data

            fu_Mysql.API_Update(id, Label_API, API_Key, API_SECRET, LineNotify,
                                PassPhrase, MarginType, ReOpenOrder)
            return redirect("/Dashboard")

        # if Create_API:
#
        #    data_User = fu_Mysql.User_select_Promo(u_id)
        #    date_ex = ""
        #    botdata_type = ""
        #    if data_User != []:
        #        try:
        #            for data in data_User:
        #                try:
        #                    date_ex = data[6]
        #                    botdata_type = data[4]
        #                except:
        #                    session["ch_Promotion"] = 'isBuy'
        #                ExpirationDate = datetime.strptime(
        #                    date_ex, "%Y-%m-%d").date()
        #                now = date.today()
        #                if ExpirationDate >= now and bot_type == botdata_type:
        #                    session["ch_Promotion"] = 'OK'
        #                    Label_API = form_dashb.Label_API.data
        #                    API_Key = form_dashb.API_Key.data
        #                    API_SECRET = form_dashb.API_SECRET.data
        #                    LineNotify = form_dashb.LineNotify.data
        #                    MarginType = form_dashb.MarginType.data
        #                    ReOpenOrder = form_dashb.ReOpenOrder.data
#
        #                    uuids = str(uuid.uuid4())
        #                    PassPhrase = uuid.uuid5(
        #                        uuid.NAMESPACE_DNS, session["UserID"]+bot_type+uuids)
#
        #                    fu_Mysql.API_insert(u_id, API_Key, API_SECRET, LineNotify, PassPhrase,
        #                                        MarginType, ReOpenOrder, "", Label_API, bot_type, "stop")
        #                    return redirect("/Dashboard")
#
        #                else:
        #                    session["ch_Promotion"] = 'isBuy'
        #                    return redirect("/Dashboard")
        #        except:
        #            session["ch_Promotion"] = 'isBuy'
        #            return redirect("/Dashboard")
    if data_alert != []:
        html_Alert = ""
        for x in data_alert:

            html_Alert += class_html.html_alert(
                x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9])

            session["html_Alert"] = html_Alert
    else:
        session["html_Alert"] = ""

    if data != []:
        htmls = ""
        html_m = ""
        html_Coins_Available = ""
        for x in data:
            try:
                data_All_Coins = Bot_Spot.Show_All_Coins_Available(x[2], x[3])

            except:
                return print("Data : don't find all coin")
            htmls += class_html.html_isbot(x[0], x[11],
                                           x[9], x[10], x[12], data_All_Coins)
            html_m += class_html.html_modal(
                x[0], x[11], x[6], x[7], x[10], x[2], x[3], x[4], x[5])
            session["html_isbot"] = htmls
            session["html_modal"] = html_m

    else:
        session["html_modal"] = ""
        session["html_isbot"] = ""

    return render_template("Dashboard.html", form=form_dashb)


@app.route("/test2", methods=["GET", "POST"])
def test2():
    print("ACTION")
    pass


@app.route("/TEST", methods=["GET", "POST"])
def test():
    forms = class_User.test_()
    u_id = session["UserID"]

    data = fu_Mysql.API_select(u_id, "", "")
    if data != []:
        htmls = ""
        html_m = ""
        html_Coins_Available = ""
        for x in data:
            try:
                # Bot_Spot.Show_All_Coins_Available(x[2], x[3])
                data_All_Coins = ["", ""]

            except:
                return print("Data : don't find all coin")
            htmls += class_html.html_isbot(x[0], x[11],
                                           x[9], x[10], x[12], data_All_Coins)
            html_m += class_html.html_modal(
                x[0], x[11], x[6], x[7], x[10], x[2], x[3], x[4], x[5])
            session["html_isbot"] = htmls
            session["html_modal"] = html_m

    else:
        session["html_modal"] = ""
        session["html_isbot"] = ""
    return render_template("TEST.html", form=forms)


@app.route("/singup", methods=["GET", "POST"])
def singup():

    form = class_User.register()
    User_login = form.Regis_UserID.data
    email = form.Regis_UserEmail.data
    Pass_login = form.Regis_User_Password.data
    Retypepass = form.Retype_password.data
    countPass = 0

    if request.method == "POST":

        data = fu_Mysql.User_select_login(User_login, "")
        print(data)
        user_indata = ''
        email_data = ''
        try:
            user_indata = data[0][1]
            email_data = data[0][2]
        except:
            pass

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

                    render_template("signup.html", form=form, name=User_login,
                                    email=email, passlogin=Pass_login, Retype_password=Retypepass)
                elif email_data == email:
                    email = "Email_already"

                    render_template("signup.html", form=form, name=User_login,
                                    email=email, passlogin=Pass_login, Retype_password=Retypepass)
                else:
                    fu_Mysql.User_create(User_login, email, hashed_Str)

                    return redirect("/login")
        else:
            if Pass_login != "len5":
                Retypepass = "dontmatch"

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


@app.route("/Billing/<string:Promotion_name>/<string:Bot_exchange>/<string:Bot_Type>/<string:Pro_price>/<string:Pro_status>/<string:Type_billing>", methods=["GET", "POST"])
def Billings(Promotion_name, Bot_exchange, Bot_Type,  Pro_price, Pro_status, Type_billing):

    u_id = session["UserID"]
    ch_demo = fu_Mysql.User_select_Promo(u_id)
    forms = class_User.Billing_s()
    x = Promotion_name
    try:
        print("*******11****[print(pos)]************")
        print(request.method)
        pos = request.args.get("buy_demo")  # forms.buy_demo.data
        print("***********[print(pos)]************")
        print(pos)
    except:
        return redirect("/Billing")
    # if ch_demo != 'demoSpot':
    #    if x == 'demoSpot' or x == 'Binace Spot 1Month' or x == 'Binace Spot 3Month' or x == 'Binace Spot 12Month' or x == 'Binace Future 1Month':
    #        fu_Mysql.User_insert_Promo(
    #            u_id, Promotion_name, Bot_exchange, Bot_Type,  Pro_price, Pro_status, Type_billing)

    return redirect("/Billing")


@app.route("/Billing", methods=["GET", "POST"])
def Billing():
    forms = class_User.Billing_s()
    if check_UserID():  # session["UserID"] == None or session["UserID"] == '':
        return redirect("/login")
    if request.method == "POST":
        pass

    return render_template("Billing.html", form=forms)


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


##################[ Send Mail ]###############
def send_mail(Email_user):
    token = password_reset_token(Email_user)

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
                return print("notfound")
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

        # ถ้า token ไม่หมดอายุให้ รอเปลี่ยน Pass

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
    form = class_User.Profile()
    if check_UserID():  # session["UserID"] == None or session["UserID"] == '':
        return redirect("/login")

    return render_template("pages-profile.html", form=form)


# --------------Bot Spot---------------------------@@@@@@@@@@@@@@@@@@@@@@@@@@@-------------------------------------


@app.route("/spot", methods=["POST"])
def Cayoshibot():
    if request.method == "POST":
        data = request.data

        Bot_Spot.CayoshiM(data)

    return ""


# --------------Bot Future---------------------------@@@@@@@@@@@@@@@@@@@@@@@@@@@-------------------------------------

@app.route('/oneway', methods=['POST', 'GET'])
def mywebhook():
    if request.method == 'POST':
        req_data = request.get_json(force=True)

        func_futures.bin_func._binanceOneway(req_data)

        return 'success', 200
    else:
        print('Signal format is incorrect.')


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
