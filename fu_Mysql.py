from select import select
import mysql.connector
from mysql.connector import Error


def connect_mysql():
    return mysql.connector.connect(host='localhost', port=3306,
                                   user='root', password='MyCayoshi88', database='hook_bot')


def User_select_login(userID, email):
    try:
        db = connect_mysql()
        cursor = db.cursor()
        sql = "call User_select('"+userID+"','"+email+"')"
        print("[@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@]")
        print(sql)
        cursor.execute(sql)
        data = cursor.fetchall()

        return(data)
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

    finally:
        cursor.close()
        db.close()


def User_create(User_id, User_Email, User_Pass):
    try:
        db = connect_mysql()
        cursor = db.cursor()
        sql = "call User_Create('"+User_id + \
            "', '" + User_Email+"' ,'"+User_Pass+"')"
        cursor.execute(sql)
        db.commit()

    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))
    finally:
        cursor.close()
        db.close()


def User_Update(where_uid, where_email, userID, email, Pass):
    try:
        db = connect_mysql()
        cursor = db.cursor()
        sql = " call User_update('" + \
            where_email+"','"+Pass+"')"
        print(sql)

        cursor.execute(sql)
        db.commit()
        print("DATA Sucseed")
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))
    finally:
        cursor.close()
        db.close()


def API_select_Active(userID):

    db = connect_mysql()
    cursor = db.cursor()

    sql = "INSERT INTO Save_Code( Keyword, Code, type) VALUES (@_Word,@_Meaning,@_comboType)"
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)

    return data


def API_create(userID, API_Key, API_SECRET, LineNotify, PassPhrase):

    db = connect_mysql()
    cursor = db.cursor()

    sql = "INSERT INTO Save_Code( Keyword, Code, type) VALUES (@_Word,@_Meaning,@_comboType)"
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)

    return data


def API_Update(userID, email, Pass,):

    db = connect_mysql()
    cursor = db.cursor()

    sql = "INSERT INTO Save_Code( Keyword, Code, type) VALUES (@_Word,@_Meaning,@_comboType)"
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)

    return data


def API_Delete(userID, email, Pass,):

    db = connect_mysql()
    cursor = db.cursor()

    sql = "DELETE FROM `hook_bot`.`tb_user_s` WHERE (`id` = '6');"
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)

    return data


def save_Alert(userID, email, Pass,):

    db = connect_mysql()
    cursor = db.cursor()

    sql = "INSERT INTO Save_Code( Keyword, Code, type) VALUES (@_Word,@_Meaning,@_comboType)"
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)

    return data


def select_Alert(userID, email, Pass,):

    db = connect_mysql()
    cursor = db.cursor()

    sql = "INSERT INTO Save_Code( Keyword, Code, type) VALUES (@_Word,@_Meaning,@_comboType)"
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)

    return data


def create_Setting_BOT(userID, email, Pass,):

    db = connect_mysql()
    cursor = db.cursor()

    sql = "INSERT INTO Save_Code( Keyword, Code, type) VALUES (@_Word,@_Meaning,@_comboType)"
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)

    return data


def update_Setting_BOT(userID, email, Pass,):

    db = connect_mysql()
    cursor = db.cursor()

    sql = "INSERT INTO Save_Code( Keyword, Code, type) VALUES (@_Word,@_Meaning,@_comboType)"
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)

    return data
