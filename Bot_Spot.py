from builtins import float
import ccxt
import json
from colorama import *
from colorama import init
from configparser import ConfigParser
from pprint import pprint
from line_notify import LineNotify
from flask import Flask, request, session
import socket
import glob
import sys
from mysql.connector import errorcode
import fu_Mysql


print(sys.path)

init()
app = Flask(__name__)
config = ConfigParser()


def Alert_error(e):

    return print("error"+e)


def CayoshiM(obj):
    #data = json.loads(datas)
    print(
        "***********************[ ActionBot ]*********************************")

    print(obj)
    try:
        data = json.loads(obj)
    except:
        Alert_error(obj)

    print(data)
    #userID = session["UserID"]
    #data_API = fu_Mysql.API_select(userID, "")
    strategy_ = ''
    price_ = ''
    side_ = ''
    Pass_in = ''
    symbol_in = ''
    Type_Order = ''
    amount_in = ''
    Label_API = ''
    Show_All_Coins_Available = ''
    line_key = ''
    Coins_value = ''
    API_KEY = ''
    API_SECRET = ''
    ifFailed = 0

    try:  # 1
        print(Fore.RED)
        try:
            strategy_ = data['strategy']
        except:
            #
            print(Fore.YELLOW+'! non format : "strategy"  ')
        try:
            price_ = data['price']
        except:
            print(Fore.YELLOW+'! non format : "price" ')

        try:
            side_ = data['side']
        except:
            print(Fore.RED+'! error format : "side" ')
        try:
            Type_Order = list(data['amount'])[0]
        except:
            print(Fore.RED+'! error format : "amount":"?123" ')
        try:
            amount_in = data['amount'][1:]
        except:
            print(Fore.RED+'! error format : "amount":"?123" ')
        try:
            symbol_in = data['symbol']
        except:
            print(Fore.RED+'! error format : "symbol" ')
        try:
            Pass_in = data['passphrase']
        except:
            print(Fore.RED+'! error format : "passphrase" ')
        print("//////////")
        print(strategy_)
        print(price_)
        print(side_)
        print(Type_Order)
        print(amount_in)
        print(symbol_in)
        print(Pass_in)
    except:
        print(Fore.RED+'===========================================================================')
        format1 = '{"side":"buy","amount":"@151","symbol":"FTMUSDT","passphrase":"pass11666"}'
        format2 = '{"side":"sell","amount":"$151","symbol":"FTMUSDT","passphrase":"pass11666"}'
        format3 = '{"side":"buy","amount":"%151","symbol":"FTMUSDT","passphrase":"pass11666"}'
        print('! error key format ')
#
        print(format1)
        print(format2)
        print(format3)
        print(Fore.RED+'===========================================================================')
        return {'! error ''side'' format ': 'error'}
