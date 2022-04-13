from select import select
import mysql.connector
from mysql.connector import Error


def connect_mysql():
    return mysql.connector.connect(host='localhost', port=3306,
                                   user='root', password='MyCayoshi88', database='hook_bot')

################################
#           [ Login User ]
################################


def User_select_login(userID, email):
    try:
        db = connect_mysql()
        cursor = db.cursor()
        sql = "call User_select('"+userID+"','"+email+"')"

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


################################
#           [ Setting_BOT ]
################################

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


################################
#           [ Alert ]
################################


def Alert_select(userID, email):
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


def Alert_insert(User_id, User_Email, User_Pass):
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

################################
#           [ API ]
################################


def API_select(userID, apikey):
    try:
        db = connect_mysql()
        cursor = db.cursor()
        sql = "call API_select('"+userID+"','"+apikey+"')"

        print("API_select Sql : " + sql)
        cursor.execute(sql)
        data = cursor.fetchall()

        return(data)
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

    finally:
        cursor.close()
        db.close()


def API_insert(user_id,  apikey,  apisecret,  linetoken_1, passphrase, margintype, reopenorder, note, label_api, bot_type, bot_status):
    try:

        db = connect_mysql()
        cursor = db.cursor()
        arr = [user_id, apikey, apisecret,  linetoken_1, passphrase,
               margintype, reopenorder, note, label_api, bot_type, bot_status]
        sql = "call API_Create('"+str(arr[0]) + "' ,'" + str(arr[1])+"' ,'" + str(arr[2])+"' ,'" + str(arr[3])+"' ,'" + str(arr[4]) + "' ,'"+str(
            arr[5])+"' ,'"+str(arr[6]) + "' ,'"+str(arr[7])+"' ,'" + str(arr[8]) + "' ,'"+str(arr[9]) + "' ,'" + str(arr[10]) + "' )"
        print("******API_insert********")
        print(sql)
        cursor.execute(sql)
        db.commit()

    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))
    finally:
        cursor.close()
        db.close()


def API_Update(id, label_api, apikey, apisecret, linetoken_1, passphrase, margintype, reopenorder):
    try:
        db = connect_mysql()
        cursor = db.cursor()
        arr = [id, label_api, apikey, apisecret, linetoken_1,
               passphrase, margintype, reopenorder]
        sql = " call API_update('"+str(arr[0]) + "' ,'" + str(arr[1])+"' ,'" + str(
            arr[2])+"' ,'" + str(arr[3])+"' ,'" + str(arr[4]) + "' ,'"+str(arr[5])+"','"+str(arr[6])+"','"+str(arr[7])+"')"
        print("***********[ API_Update ]************")
        print(sql)

        cursor.execute(sql)
        db.commit()
        print("DATA Sucseed")
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))
    finally:
        cursor.close()
        db.close()


def API_Delete(bot_id):
    try:
        db = connect_mysql()
        cursor = db.cursor()
        sql = " call API_Delete('" + bot_id+"')"
        print(sql)

        cursor.execute(sql)
        db.commit()
        print("DATA Sucseed")
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))
    finally:
        cursor.close()
        db.close()


def API_PauseOrRun(id, status):
    try:
        db = connect_mysql()
        cursor = db.cursor()
        sql = "call API_PauseOrRun( '"+id+"' ,'" + status+"')"
        print(sql)

        cursor.execute(sql)
        db.commit()
        print("DATA Sucseed")
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))
    finally:
        cursor.close()
        db.close()
################################
#           [ Billing ]
################################


def Billing_select(userID, email):
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


def Billing_insert(User_id, User_Email, User_Pass):
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
