import os
import json
import ccxt
# import sys
import requests
import time
import math
import mysql.connector


from datetime import datetime, date, timedelta
from colorama import init
from pprint import pprint

from flask import Flask, request, abort, send_file
from mysql.connector import errorcode

init()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    Tblack = '\033[30m'
    Tred = '\033[31m'
    Tgreen = '\033[32m'
    Tyellow = '\033[33m'
    Tblue = '\033[34m'
    Tmagenta = '\033[35m'
    Tcyan = '\033[36m'
    Twhite = '\033[37m'
    TBcyan_magenta = '\033[36;45;1m'
    TBblack_white = '\033[30;47;1m'
    TBred_white = '\033[31;47;1m'
    TBgreen_white = '\033[32;47;1m'
    TByellow_white = '\033[33;47;1m'
    TBblue_white = '\033[34;47;1m'
    TBmagenta_white = '\033[35;47;1m'


def mysqlselect(sql):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(sql)
    columns = cursor.description
    result = []
    for value in cursor.fetchall():
        tmp = {}
        for (index, column) in enumerate(value):
            tmp[columns[index][0]] = column
        result.append(tmp)
    cursor.close()
    cnx.close()
    return result


def lineNotify(message, file=None, LineNotify=None):
    payload = {'message': message}
    url = 'https://notify-api.line.me/api/notify'
    token = LineNotify
    headers = {'Authorization': 'Bearer ' + token}
    return requests.post(url, headers=headers, data=payload, files=file)


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier


def re_quantity(re_base, quantity, filter):
    minQty = float(filter['minQty'])
    stepSize = float(filter['stepSize'])
    quantity = float(round_down(quantity, len(str(stepSize))-2))
    # output = '{: .5f}'.format(stepSize)
    # print('%f' % minQty,output)
    cal_quantity = quantity - ((quantity - minQty) % stepSize)
    if (len(str(cal_quantity)) >= 5):
        re_ans = round_up(cal_quantity, len(str(stepSize))-2)
        if (re_base == 'BTC'):
            floating = re_ans
            strfloating = str(floating)
            index1 = strfloating.find('e')
            if (index1 > 0):
                num = strfloating[index1 + 1:]
                floated = format(floating, '.6f')
                return floated
            else:
                return float(floating)
    else:
        re_ans = cal_quantity
    return re_ans


def tv_conv_buy(amount, f_balance, l_price, s_leverage):
    # Check free_balance
    # print(amount, f_balance, l_price, s_leverage)
    if (amount[0:1].isalnum()):
        ans = amount
        return ans
    ans = float(amount[1:len(amount)])
    c_amount = (ans / l_price * s_leverage)
    p_amount = (f_balance / l_price * s_leverage) * (ans / 100)
    pt_amount = (f_balance / l_price * s_leverage) * (100 / 100)
    a_amount = ans
    if (amount[0:1] == '$'):
        if (pt_amount > c_amount):
            ans = c_amount
        else:
            ans = pt_amount
    elif (amount[0:1] == '%'):
        if (ans < 100):
            ans = p_amount
        else:
            ans = pt_amount
    elif (amount[0:1] == '@'):
        if (pt_amount > a_amount):
            ans = a_amount
        else:
            ans = pt_amount
    else:
        ans = ans
    return ans


def tv_conv_sell(amount, pt_amount, l_price, s_leverage):
    # Check position_amount
    # print(amount, pt_amount, l_price, s_leverage)
    if(float(pt_amount) == 0):
        print(bcolors.Tred + 'No Position.' + bcolors.ENDC)
        return 0
    if (amount[0:1].isalnum()):
        ans = amount
        return ans
    ans = float(amount[1:len(amount)])
    c_amount = (ans / l_price * s_leverage)
    p_amount = (pt_amount) * (ans / 100)
    a_amount = ans
    if (amount[0:1] == '$'):
        if (pt_amount > c_amount):
            ans = c_amount
        else:
            ans = pt_amount
    elif (amount[0:1] == '%'):
        if (ans < 100):
            ans = p_amount
        else:
            ans = pt_amount
    elif (amount[0:1] == '@'):
        if (pt_amount > a_amount):
            ans = a_amount
        else:
            ans = pt_amount
    else:
        ans = ans
    return ans


def sr(num_):
    return str(round_down(num_, 4))


def convert_symbol(symbol):
    symbol = symbol.replace('/', '')
    index1 = symbol.find('BUSD')
    if (index1 > 1):
        base = symbol[:index1]
        quote = symbol[index1:]
        index2 = quote.find('PERP')
        if (index2 > 2):
            quote = quote[:index2]
    index1 = symbol.find('USDT')
    if (index1 > 1):
        base = symbol[:index1]
        quote = symbol[index1:]
        index2 = quote.find('PERP')
        if (index2 > 2):
            quote = quote[:index2]
    c_symbol = base + '/' + quote
    n_symbol = base + quote
    # print(c_symbol,n_symbol,base,quote)
    return [c_symbol, n_symbol, base, quote]


def _binanceFutures(data, configLoaded):
    print(bcolors.OKBLUE + '\n***************************************************************************************' + bcolors.ENDC)
    json_data = json.dumps(data)
    json_data1 = json.loads(json_data)
    hidepass = ''
    for i in range(len(json_data1['passphrase'])):
        hidepass += '*'
    json_data1['passphrase'] = hidepass
    print(bcolors.Tcyan + json.dumps(json_data1) + bcolors.ENDC)
    try:
        exchange = ccxt.binance({
            'apiKey': configLoaded['binance_apikey'],
            'secret': configLoaded['binance_secret'],
            'enableRateLimit': True,  # https://github.com/ccxt/ccxt/wiki/Manual#rate-limit
            'timeout': 3000,
            'options': {
                'defaultType': 'future',
                'adjustForTimeDifference': True
            }
        })

    except:
        print('Binance Error (API,Mode)')

    # print('Changing your', data['symbol'], 'position margin mode to CROSSED:ISOLATED')
    try:
        response = exchange.fapiPrivate_post_margintype({
            'symbol': convert_symbol(data['symbol'])[1],
            'marginType': configLoaded['margintype'],
        })
    except:
        print('Binance Error (Symbol,Margintype)')
    try:
        response = exchange.fapiPrivate_post_positionside_dual({
            'dualSidePosition': False,
        })
    except:
        print('Binance Error (Isolated,Crossed)')
    time.sleep(0.1)
    markets = exchange.load_markets()
    exchange.verbose = False
    market = exchange.market(convert_symbol(data['symbol'])[0])
    filters2 = (market['info']['filters'][2])
    fBalance = exchange.fetch_balance().get(
        convert_symbol(data['symbol'])[3]).get('free')
    sBalance = exchange.fetch_balance().get(
        convert_symbol(data['symbol'])[3]).get('total')
    LastPrice = float(exchange.fetchTicker(
        convert_symbol(data['symbol'])[0]).get('last'))
    symbol_leverage = (exchange.fetch_positions(
        convert_symbol(data['symbol'])[0])[0]['info']['leverage'])
    print(bcolors.Tyellow + 'You are in ' + exchange.fetch_positions(convert_symbol(data['symbol'])[
          0])[0]['info']['marginType'] + ' ' + str(int(symbol_leverage)) + 'x' + bcolors.ENDC)
    get_pos = exchange.fetch_positions(convert_symbol(data['symbol'])[0])
    time.sleep(0.1)
    print(bcolors.Tmagenta + 'Balance\t:  ' + sr(fBalance) + '/' +
          sr(sBalance) + ' ' + convert_symbol(data['symbol'])[3] + bcolors.ENDC)
    if (get_pos != None):
        pos_side = get_pos[0]['side']
        pos_amount = get_pos[0]['contracts']
        # print(pos_side,pos_amount)
    if (data['side'] == 'OpenLong') or (data['side'] == 'openlong') or (data['side'] == 'buy') or (data['side'] == 'LONG') or (data['side'] == 'Long') or (data['side'] == 'long') or (data['side'] == 'L'):
        # and (get_pos[0]['contracts'] != 0.0):
        if ((configLoaded['reopenorder'] == 'off') or (configLoaded['reopenorder'] == 'OFF')) and (pos_side == 'long'):
            print(bcolors.Tmagenta +
                  'You have position. Bot no Open Order.' + bcolors.ENDC)
            return -2
        if (pos_side == 'short'):
            print(bcolors.Tred + 'CloseShort' + bcolors.ENDC)
            response = exchange.create_order(convert_symbol(data['symbol'])[
                                             0], 'MARKET', 'BUY', pos_amount, None, {'reduceOnly': True})
            time.sleep(0.1)
        print(bcolors.Tgreen + 'OpenLong' + bcolors.ENDC)
        buy_quantity = (re_quantity(convert_symbol(data['symbol'])[2], float(
            tv_conv_buy(data['amount'], fBalance, LastPrice, symbol_leverage)), filters2))
        response = exchange.create_order(convert_symbol(data['symbol'])[
                                         0], 'MARKET', 'BUY', buy_quantity, None)
    elif (data['side'] == 'OpenShort') or (data['side'] == 'openshort') or (data['side'] == 'sell') or (data['side'] == 'SHORT') or (data['side'] == 'Short') or (data['side'] == 'short') or (data['side'] == 'S'):
        # and (get_pos[0]['contracts'] != 0.0):
        if ((configLoaded['reopenorder'] == 'off') or (configLoaded['reopenorder'] == 'OFF')) and (pos_side == 'short'):
            print(bcolors.Tmagenta +
                  'You have position. Bot no Open Order.' + bcolors.ENDC)
            return -2
        if (pos_side == 'long'):
            print(bcolors.Tgreen + 'CloseLong' + bcolors.ENDC)
            response = exchange.create_order(convert_symbol(data['symbol'])[
                                             0], 'MARKET', 'SELL', pos_amount, None, {'reduceOnly': True})
            time.sleep(0.1)
        print(bcolors.Tred + 'OpenShort' + bcolors.ENDC)
        buy_quantity = (re_quantity(convert_symbol(data['symbol'])[2], float(
            tv_conv_buy(data['amount'], fBalance, LastPrice, symbol_leverage)), filters2))
        response = exchange.create_order(convert_symbol(data['symbol'])[
                                         0], 'MARKET', 'SELL', buy_quantity, None)
    elif (data['side'] == 'CloseLong') or (data['side'] == 'closelong') or (data['side'] == 'CL'):
        print(bcolors.Tgreen + 'CloseLong' + bcolors.ENDC)
        if (get_pos == None):
            print(bcolors.Tmagenta +
                  "You don't have position. Bot no Close Order." + bcolors.ENDC)
            return -3
        if (data['amount'] == '%100'):
            response = exchange.create_order(convert_symbol(data['symbol'])[
                                             0], 'MARKET', 'SELL', pos_amount, None, {'reduceOnly': True})
        else:
            sell_long_quantity = (re_quantity(convert_symbol(data['symbol'])[2], float(tv_conv_sell(
                data['amount'], get_pos[0]['contracts'], LastPrice, symbol_leverage)), filters2))
            response = exchange.create_order(convert_symbol(data['symbol'])[
                                             0], 'MARKET', 'SELL', sell_long_quantity, None)
    elif (data['side'] == 'CloseShort') or (data['side'] == 'closeshort') or (data['side'] == 'CS'):
        print(bcolors.Tred + 'CloseShort' + bcolors.ENDC)
        if (get_pos == None):
            print(bcolors.Tmagenta +
                  "You don't have position. Bot no Close Order." + bcolors.ENDC)
            return -3
        if (data['amount'] == '%100'):
            response = exchange.create_order(convert_symbol(data['symbol'])[
                                             0], 'MARKET', 'BUY', pos_amount, None, {'reduceOnly': True})
        else:
            sell_short_quantity = (re_quantity(convert_symbol(data['symbol'])[2], float(tv_conv_sell(
                data['amount'], get_pos[0]['contracts'], LastPrice, symbol_leverage)), filters2))
            response = exchange.create_order(convert_symbol(data['symbol'])[
                                             0], 'MARKET', 'BUY', sell_short_quantity, None)
    elif (data['side'] == 'CloseLongOpenShort') or (data['side'] == 'closelongopenshort'):
        print(bcolors.Tgreen + 'CloseLong' + bcolors.ENDC)
        if (pos_amount == 0.0):
            print(bcolors.Tmagenta +
                  "You don't have position. Bot no Close Order." + bcolors.ENDC)
        elif (pos_amount != 0.0) and (pos_side == 'long'):
            response = exchange.create_order(convert_symbol(data['symbol'])[
                                             0], 'MARKET', 'SELL', pos_amount, None, {'reduceOnly': True})
        time.sleep(0.2)
        print(bcolors.Tred + 'OpenShort' + bcolors.ENDC)
        buy_quantity = (re_quantity(convert_symbol(data['symbol'])[2], float(
            tv_conv_buy(data['amount'], fBalance, LastPrice, symbol_leverage)), filters2))
        response = exchange.create_order(convert_symbol(data['symbol'])[
                                         0], 'MARKET', 'SELL', buy_quantity, None)
    elif (data['side'] == 'CloseShortOpenLong') or (data['side'] == 'closeshortopenlong'):
        print(bcolors.Tred + 'CloseShort' + bcolors.ENDC)
        if (pos_amount == 0.0):
            print(bcolors.Tmagenta +
                  "You don't have position. Bot no Close Order." + bcolors.ENDC)
        elif (pos_amount != 0.0) and (pos_side == 'short'):
            response = exchange.create_order(convert_symbol(data['symbol'])[
                                             0], 'MARKET', 'BUY', pos_amount, None, {'reduceOnly': True})
        time.sleep(0.2)
        print(bcolors.Tgreen + 'OpenLong' + bcolors.ENDC)
        buy_quantity = (re_quantity(convert_symbol(data['symbol'])[2], float(
            tv_conv_buy(data['amount'], fBalance, LastPrice, symbol_leverage)), filters2))
        response = exchange.create_order(convert_symbol(data['symbol'])[
                                         0], 'MARKET', 'BUY', buy_quantity, None)
    else:
        print(bcolors.Tred + 'Position Order Failed.' + bcolors.ENDC)
    time.sleep(1)
    try:
        print(bcolors.Tmagenta +
              "{:<10} {:<10} {:<10} {:<10}".format('Symbol', 'Amount', 'Price', 'Side'))
        print("{:<10} {:<10} {:<10} {:<10}".format(
            response['symbol'], response['amount'], response['price'], response['side']) + bcolors.ENDC)
        print(bcolors.OKBLUE + '***************************************************************************************' + bcolors.ENDC)
        mesg = '\n' + chr(128640) + 'BinanceⓂOneWay' + chr(128640) + '\nCoin      : ' + response['symbol'] + '\nStatus   : ' + response['side'].upper() + ' [' + data['side'] + ']\nAmount : ' + str(response['amount']) + ' ' + convert_symbol(data['symbol'])[2] + '\nPrice     : ' + str(
            response['price']) + ' USD'
        lineNotify(mesg, None, configLoaded['line_notify'])
        return (response)
    except:
        print('Response Error !!!')

    return -9999


trx = 'TXrgXCzDnYKtUVZQKbXHktUqCuhEZTTFoq'
print(bcolors.Tyellow + 'Donation :')
print('TRON(TRX) wallet : ' + trx + '\n' + bcolors.ENDC)

config = {
    'host': 'localhost',
    'port': 3306,
    'database': 'botbinance01',
    'user': 'botbinance01',
    'password': '00000000',
    'charset': 'utf8',
    'use_unicode': True,
    'get_warnings': True,
}

now = datetime.now()
strDate = str(now.strftime('%d%m%Y'))

app = Flask(__name__)

# @app.route('/')
# def index():
#     return abort(400)

# @app.route('/status')
# def status():
#     webmessage = "on"
#     return webmessage
###########################################################################################################################################################################################
###########################################################################################################################################################################################

# @app.route('/mybotnaja', methods=['POST','GET'])


def mywebhook():
    if request.method == 'GET':
        webmessage = '<h1>Hello from Bot NaJa!</h1>Tradingview Webhook URL put ->  http://' + \
            request.environ['HTTP_HOST'] + '/mybotnaja<br>{"side": "OpenLong", "amount": "@0.02", "symbol": "{{ticker}}", "uname":"username", "passphrase": "1234"}<br>{"side": "OpenShort", "amount": "$0.02", "symbol": "{{ticker}}", "uname":"username", "passphrase": "1234"}<br>{"side": "CloseLong", "amount": "%0.02", "symbol": "{{ticker}}", "uname":"username", "passphrase": "1234"}<br>{"side": "CloseShort", "amount": "@0.02", "symbol": "{{ticker}}", "uname":"username", "passphrase": "1234"}'
        return webmessage
    if request.method == 'POST':
        req_data = request.get_json(force=True)
        # file that webhook payloads will be written
        filename = str(req_data['uname']) + '_dataLog_' + strDate + '.txt'
        if os.path.exists(filename):
            append_write = 'a'  # append if already exists
        else:
            append_write = 'w'  # make a new file if not
        f = open(filename, append_write)
        strTime = str(now.strftime('%d/%m/%Y %H:%M:%S') + '  ')
        if (req_data != None):
            str_obj = json.dumps(req_data)
            f.write(strTime + str_obj + '\n')
        f.close()

        username = req_data['uname']
        passphrase = req_data['passphrase']
        sql = "SELECT * FROM `config2bot` WHERE username='" + \
            username + "' AND passphrase='" + passphrase + "'"
        configLoaded = mysqlselect(sql)[0]

        if (req_data['passphrase'] == configLoaded['passphrase']):
            # print('Password OK')
            try:
                (_binanceFutures(req_data, configLoaded))
            except OSError:
                print('Goto Binance again')
        return 'success', 200
    else:
        abort(400)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=80, threaded=True, debug=False)
