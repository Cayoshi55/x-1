from functools import cache
import os
import math
import json
import re
import time
import requests
import logging
import mysql.connector
import ccxt
import fu_Mysql

from pprint import pprint
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("func_debug.log"),
        logging.StreamHandler()
    ]
)


class bin_func():
    def __init__(self, json_data):
        self.json_data = json_data

    def mysqlselect_user(passphrase):
        sql = "SELECT * FROM `tb_user_api` WHERE passphrase='" + passphrase + "'"
        # print(sql)
        conf_mysql = {
            'host': 'localhost',
            'port': 3306,
            'database': 'hook_bot',
            'user': 'root',
            'password': 'MyCayoshi88',
            'charset': 'utf8',
            'use_unicode': True,
            'get_warnings': True,
        }
        cnx = mysql.connector.connect(**conf_mysql)
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

    # def mysqlselect(sql):
    #     # conf_mysql = {
    #     #     'host': 'localhost',
    #     #     'port': 3306,
    #     #     'database': 'botbinance01',
    #     #     'user': 'botbinance01',
    #     #     'password': '00000000',
    #     #     'charset': 'utf8',
    #     #     'use_unicode': True,
    #     #     'get_warnings': True,
    #     # }
    #     cnx = mysql.connector.connect(**conf_server.conf_mysql)
    #     cursor = cnx.cursor()
    #     cursor.execute(sql)
    #     columns = cursor.description
    #     result = []
    #     for value in cursor.fetchall():
    #         tmp = {}
    #         for (index, column) in enumerate(value):
    #             tmp[columns[index][0]] = column
    #         result.append(tmp)
    #     cursor.close()
    #     cnx.close()
    #     return result

    def lineNotify(message, file=None, LineNotify=None):

        payload = {'message': message}
        url = 'https://notify-api.line.me/api/notify'
        token = LineNotify
        headers = {'Authorization': 'Bearer ' + token}
        response = requests.post(url, headers=headers,
                                 data=payload, files=file)
        if (str(response) == '<Response [401]>'):
            print('LineNotify token Error.')
        return (response)

    # def sr(num_):
    #     return str(self.round_down(num_, 4))

    def round_up(n, decimals=0):
        multiplier = 10 ** decimals
        return math.ceil(n * multiplier) / multiplier

    def round_down(n, decimals=0):
        multiplier = 10 ** decimals
        return math.floor(n * multiplier) / multiplier

    def re_quantity(re_base, quantity, filter):
        minQty = float(filter['minQty'])
        stepSize = float(filter['stepSize'])
        quantity = float(bin_func.round_down(quantity, len(str(stepSize)) - 2))
        # output = '{: .5f}'.format(stepSize)
        # print('%f' % minQty,output)
        cal_quantity = quantity - ((quantity - minQty) % stepSize)
        if (len(str(cal_quantity)) >= 5):
            re_ans = bin_func.round_up(cal_quantity, len(str(stepSize)) - 2)
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
        if (float(pt_amount) == 0):
            print('No Position.')
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

    def convert_symbol(symbol):
        print("*********[convert_symbol]**********")
        print(symbol)
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
        try:
            c_symbol = base + '/' + quote
        except:
            return print("def convert_symbol :line 207")
        n_symbol = base + quote
        return [c_symbol, n_symbol, base, quote]

    def user_signal_log(data, configLoaded):
        now = datetime.now()
        strDate = str(now.strftime('%d%m%Y'))
        # filename = str(req_data['uname']) + '_dataLog_' + strDate + '.txt'  # file that webhook payloads will be written
        # file that webhook payloads will be written
        filename = str(configLoaded['user_id']) + \
            '_dataLog_' + strDate + '.txt'
        if os.path.exists(filename):
            append_write = 'a'  # append if already exists
        else:
            append_write = 'w'  # make a new file if not
        f = open(filename, append_write)
        strTime = str(now.strftime('%d/%m/%Y %H:%M:%S') + '  ')
        if (data != None):
            str_obj = json.dumps(data)
            f.write(strTime + str_obj + '\n')
        f.close()
        return 'user_signal_log_worked'

    def binance_err(error):
        j_error = json.loads(error[8:])
        code = j_error['code']
        msg = j_error['msg']
        return [code, msg]

    def _binanceOneway(data):   # configLoaded
        print('\n***************************************************************************************')
        configLoaded = bin_func.mysqlselect_user(data['passphrase'])
        if configLoaded == []:
            print('No data in database.')
            return -1
        else:
            configLoaded = configLoaded[0]

        bin_func.user_signal_log(data, configLoaded)

        json_data = json.dumps(data)
        json_data1 = json.loads(json_data)
        hidepass = ''
        for i in range(len(json_data1['passphrase'])):
            hidepass += '*'
        json_data1['passphrase'] = hidepass

        print(json.dumps(json_data1))
        print(data['symbol'])
        t_symbol = bin_func.convert_symbol(data['symbol'])
        print((t_symbol))
        if t_symbol != None:
            symbol_ = t_symbol[0]
            symbol = t_symbol[1]
            base = t_symbol[2]
            quote = t_symbol[3]
            cmmd = data['side'].lower()
            cmmd_check = False
            cmmd_list = ['openlong', 'long', 'l', 'buy', 'closelong',
                         'cl', 'openshort', 'short', 's', 'sell', 'closeshort', 'cs']
        else:
            return print("t_symbol = None : 257")
        for c in cmmd_list:
            if (c == cmmd):
                cmmd_check = True
        if (cmmd_check == False):
            print('Bot unknow this command.')
            return -1

        try:
            exchange = ccxt.binance({
                'apiKey': configLoaded['apikey'],
                'secret': configLoaded['apisecret'],
                'enableRateLimit': True,  # https://github.com/ccxt/ccxt/wiki/Manual#rate-limit
                'timeout': 3000,
                'options': {
                    'defaultType': 'future',
                    'adjustForTimeDifference': True
                }
            })
        except Exception as e:
            print('Binance API error -> ', e)
            # print('Binance Error (API,Mode)')

        # print('Changing your', data['symbol'], 'position margin mode to CROSSED:ISOLATED')
        try:
            response = exchange.fapiPrivate_post_margintype({
                'symbol': symbol,
                'marginType': configLoaded['margintype'],
            })
            print('Margin mode is changed.')
        except Exception as e:
            if bin_func.binance_err(str(e))[0] == -4046:
                e = ''  # Margin correct.
            elif bin_func.binance_err(str(e))[0] == -1121:
                print('\nBinance does not have market symbol ' + symbol_)
                bin_func.lineNotify(
                    ('ชื่อคู่เหรียญไม่ถูกต้อง ' + symbol_), None, configLoaded['linetoken_1'])
                return -2
            elif bin_func.binance_err(str(e))[0] == -1022:
                print('\nBinance API_SECERT error.')
                bin_func.lineNotify(
                    ('Binance API_SECERT ไม่ถูกต้อง.'), None, configLoaded['linetoken_1'])
                return -2
            elif bin_func.binance_err(str(e))[0] == -2014:
                print('\nBinance API_KEY error.')
                bin_func.lineNotify(
                    ('Binance API_KEY ไม่ถูกต้อง.'), None, configLoaded['linetoken_1'])
                return -2
            elif bin_func.binance_err(str(e))[0] == -1021:
                print('\nBinance Timestamp for this request error.')
                bin_func.lineNotify(
                    ('กรุณาตั้งเวลาเครื่องServerใหม่'), None, configLoaded['linetoken_1'])
                return -2
            else:
                print('\nBinance error at ISOLATED/CROSSED -> ', str(e))
                bin_func.lineNotify(
                    ('Binance error at ISOLATED/CROSSED -> ', str(e)), None, configLoaded['linetoken_1'])
        try:
            response = exchange.fapiPrivate_post_positionside_dual({
                'dualSidePosition': False,
            })
        except Exception as e:
            if bin_func.binance_err(str(e))[0] == -4059:
                e = ''  # Position side correct.
            elif bin_func.binance_err(str(e))[0] == -1121:
                print('\nBinance does not have market symbol ' + symbol_)
                bin_func.lineNotify(
                    ('Binance does not have market symbol ' + symbol_), None, configLoaded['linetoken_1'])
                return -2
            elif bin_func.binance_err(str(e))[0] == -1022:
                print('\nBinance API_SECERT error.')
                bin_func.lineNotify(
                    ('Binance API_SECERT error.'), None, configLoaded['linetoken_1'])
                return -2
            elif bin_func.binance_err(str(e))[0] == -2014:
                print('\nBinance API_KEY error.')
                bin_func.lineNotify(('Binance API_KEY error.'),
                                    None, configLoaded['linetoken_1'])
                return -2
            elif bin_func.binance_err(str(e))[0] == -1021:
                print('\nBinance Timestamp for this request error.')
                bin_func.lineNotify(
                    ('Binance Timestamp for this request error.'), None, configLoaded['linetoken_1'])
                return -2
            else:
                print('\nBinance error at Oneway/Hedge -> ', str(e))
                bin_func.lineNotify(
                    ('Binance error at ISOLATED/CROSSED -> ', str(e)), None, configLoaded['linetoken_1'])

        time.sleep(0.1)
        markets = exchange.load_markets()
        exchange.verbose = False
        try:
            market = exchange.market(symbol_)
        except Exception as e:
            if bin_func.binance_err(str(e))[0] == -4059:
                e = ''  # Position side correct.
            elif bin_func.binance_err(str(e))[0] == -1121:
                print('\nBinance does not have market symbol ' + symbol_)
                bin_func.lineNotify(
                    ('Binance does not have market symbol ' + symbol_), None, configLoaded['linetoken_1'])
                return -2
            elif bin_func.binance_err(str(e))[0] == -1022:
                print('\nBinance API_SECERT error.')
                bin_func.lineNotify(
                    ('Binance API_SECERT error.'), None, configLoaded['linetoken_1'])
                return -2
            elif bin_func.binance_err(str(e))[0] == -2014:
                print('\nBinance API_KEY error.')
                bin_func.lineNotify(('Binance API_KEY error.'),
                                    None, configLoaded['linetoken_1'])
                return -2
            elif bin_func.binance_err(str(e))[0] == -1021:
                print('\nBinance Timestamp for this request error.')
                bin_func.lineNotify(
                    ('Binance Timestamp for this request error.'), None, configLoaded['linetoken_1'])
                return -2
            else:
                print('\nBinance does not have market symbol ' +
                      symbol_ + ' -> ', str(e))

        filters2 = (market['info']['filters'][2])
        fBalance = exchange.fetch_balance().get(quote).get('free')
        sBalance = exchange.fetch_balance().get(quote).get('total')
        LastPrice = float(exchange.fetchTicker(symbol_).get('last'))
        symbol_leverage = float(exchange.fetch_positions(symbol_)[
                                0]['info']['leverage'])
        print('You are in ' + exchange.fetch_positions(symbol_)
              [0]['info']['marginType'] + ' ' + str(int(symbol_leverage)) + 'x')
        get_pos = exchange.fetch_positions(symbol_)
        time.sleep(0.1)
        print("Balance\t:  {:.4f}/{:.4f} {}".format(fBalance, sBalance, quote))
        if (get_pos != None):
            pos_side = get_pos[0]['side']
            pos_amount = get_pos[0]['contracts']
            # print(pos_side,pos_amount)
        if (data['side'].lower() == 'openlong') or (data['side'].lower() == 'buy') or (data['side'].lower() == 'long') or (data['side'].lower() == 'l'):
            if (configLoaded['reopenorder'].lower() == 'off') and (pos_side == 'long'):
                print("You have Long position. Bot doesn't have Open Order.")
                return -2
            if (pos_side == 'short'):
                print('signal  : CloseShort')
                response = exchange.create_order(
                    symbol_, 'MARKET', 'BUY', pos_amount, None, {'reduceOnly': True})
                time.sleep(0.1)
            print('signal  : OpenLong')
            buy_quantity = (bin_func.re_quantity(base, float(bin_func.tv_conv_buy(
                data['amount'], fBalance, LastPrice, symbol_leverage)), filters2))
            try:
                response = exchange.create_order(
                    symbol_, 'MARKET', 'BUY', buy_quantity, None)
            except Exception as e:
                if bin_func.binance_err(str(e))[0] == -4164:
                    print("You have less amount for position. Bot doesn't Open Order.")
                    bin_func.lineNotify(
                        ("\nCoin : " + data['symbol'] + "\nAmountของPostionน้อยไป"), None, configLoaded['linetoken_1'])
                else:
                    print('Binance Order command error -> ', str(e))
        elif (data['side'].lower() == 'openshort') or (data['side'].lower() == 'sell') or (data['side'].lower() == 'short') or (data['side'].lower() == 's'):
            if (configLoaded['reopenorder'].lower() == 'off') and (pos_side == 'short'):
                print("You have Short position. Bot doesn't have Open Order.")
                return -2
            if (pos_side == 'long'):
                print('signal  : CloseLong')
                response = exchange.create_order(
                    symbol_, 'MARKET', 'SELL', pos_amount, None, {'reduceOnly': True})
                time.sleep(0.1)
            print('signal  : OpenShort')
            buy_quantity = (bin_func.re_quantity(base, float(bin_func.tv_conv_buy(
                data['amount'], fBalance, LastPrice, symbol_leverage)), filters2))
            try:
                response = exchange.create_order(
                    symbol_, 'MARKET', 'SELL', buy_quantity, None)
            except Exception as e:
                if bin_func.binance_err(str(e))[0] == -4164:
                    print("You have less amount for position. Bot doesn't Open Order.")
                    bin_func.lineNotify(
                        ("\nCoin : " + data['symbol'] + "\nAmountของPostionน้อยไป"), None, configLoaded['linetoken_1'])
                else:
                    print('Binance Order command error -> ', str(e))
        elif (data['side'].lower() == 'closelong') or (data['side'].lower() == 'cl'):
            print('signal  : CloseLong')
            if (pos_side == None):
                print("You don't have position. Bot doesn't Close Order.")
                return -3
            if (data['amount'] == '%100'):
                response = exchange.create_order(
                    symbol_, 'MARKET', 'SELL', pos_amount, None, {'reduceOnly': True})
            else:
                sell_long_quantity = (bin_func.re_quantity(base, float(bin_func.tv_conv_sell(
                    data['amount'], get_pos[0]['contracts'], LastPrice, symbol_leverage)), filters2))
                try:
                    response = exchange.create_order(
                        symbol_, 'MARKET', 'SELL', sell_long_quantity, None)
                except Exception as e:
                    if bin_func.binance_err(str(e))[0] == -4164:
                        print(
                            "You have less amount for position. Bot doesn't Open Order.")
                        bin_func.lineNotify(
                            ("\nCoin : " + data['symbol'] + "\nAmountของPostionน้อยไป"), None, configLoaded['linetoken_1'])
                    else:
                        print('Binance Order command error -> ', str(e))
        elif (data['side'].lower() == 'closeshort') or (data['side'].lower() == 'cs'):
            print('signal  : CloseShort')
            if (pos_side == None):
                print("You don't have position. Bot doesn't Close Order.")
                return -3
            if (data['amount'] == '%100'):
                response = exchange.create_order(
                    symbol_, 'MARKET', 'BUY', pos_amount, None, {'reduceOnly': True})
            else:
                sell_short_quantity = (bin_func.re_quantity(base, float(bin_func.tv_conv_sell(
                    data['amount'], get_pos[0]['contracts'], LastPrice, symbol_leverage)), filters2))
                try:
                    response = exchange.create_order(
                        symbol_, 'MARKET', 'BUY', sell_short_quantity, None)
                except Exception as e:
                    if bin_func.binance_err(str(e))[0] == -4164:
                        print(
                            "You have less amount for position. Bot doesn't Open Order.")
                        bin_func.lineNotify(
                            ("\nCoin : " + data['symbol'] + "\nAmountของPostionน้อยไป"), None, configLoaded['linetoken_1'])
                    else:
                        print('Binance Order command error -> ', str(e))
        elif (data['side'].lower() == 'closelongopenshort'):
            print('signal  : CloseLong')
            if (pos_side == None):
                print("You don't have position. Bot doesn't Close Order.")
            elif (pos_amount != 0.0) and (pos_side == 'long'):
                response = exchange.create_order(
                    symbol_, 'MARKET', 'SELL', pos_amount, None, {'reduceOnly': True})
            time.sleep(0.2)
            print('signal  : OpenShort')
            buy_quantity = (bin_func.re_quantity(base, float(bin_func.tv_conv_buy(
                data['amount'], fBalance, LastPrice, symbol_leverage)), filters2))
            try:
                response = exchange.create_order(
                    symbol_, 'MARKET', 'SELL', buy_quantity, None)
            except Exception as e:
                if bin_func.binance_err(str(e))[0] == -4164:
                    print("You have less amount for position. Bot doesn't Open Order.")
                    bin_func.lineNotify(
                        ("\nCoin : " + data['symbol'] + "\nAmountของPostionน้อยไป"), None, configLoaded['linetoken_1'])
                else:
                    print('Binance Order command error -> ', str(e))
        elif (data['side'].lower() == 'closeshortopenlong'):
            print('signal  : CloseShort')
            if (pos_side == None):
                print("You don't have position. Bot doesn't Close Order.")
            elif (pos_amount != 0.0) and (pos_side == 'short'):
                response = exchange.create_order(
                    symbol_, 'MARKET', 'BUY', pos_amount, None, {'reduceOnly': True})
            time.sleep(0.2)
            print('signal  : OpenLong')
            buy_quantity = (bin_func.re_quantity(base, float(bin_func.tv_conv_buy(
                data['amount'], fBalance, LastPrice, symbol_leverage)), filters2))
            try:
                response = exchange.create_order(
                    symbol_, 'MARKET', 'BUY', buy_quantity, None)
            except Exception as e:
                if bin_func.binance_err(str(e))[0] == -4164:
                    print("You have less amount for position. Bot doesn't Open Order.")
                    bin_func.lineNotify(
                        ("\nCoin : " + data['symbol'] + "\nAmountของPostionน้อยไป"), None, configLoaded['linetoken_1'])
                else:
                    print('Binance Order command error -> ', str(e))
        else:
            print('Position Order Failed.')
        time.sleep(1)
        try:
            mesg = '\n' + chr(128640) + 'BinanceⓂOneWay' + chr(128640) + '\nCoin      : ' + response[
                'symbol'] + '\nStatus   : ' + response['side'].upper() + ' [' + data['side'] + ']\nAmount : ' + str(
                response['amount']) + ' ' + base + ' ' + data['amount'] + '\nPrice     : ' + str(
                response['price']) + ' USD'
            (bin_func.lineNotify(mesg, None, configLoaded['linetoken_1']))

            fu_Mysql.Alert_insert(user_id, apikey, botAction, price,
                                  side, amount, symbol, passphrase, strategy_name)

            print("{:<10} {:<10} {:<10} {:<10}".format(
                'Symbol', 'Amount', 'Price', 'Side'))
            print("{:<10} {:<10} {:<10} {:<10}".format(response['symbol'], response['amount'], response['price'],
                                                       response['side']))
            print(
                '***************************************************************************************')
            return (response)
        except:
            print('Response Error !!!')

        return -9999
