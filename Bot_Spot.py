from array import array
from builtins import float
from distutils.log import info
import this
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
# ยังไม่ได้เช็กเงินไม่พอซื้อ เหรียญไม่พอขาย

app = Flask(__name__)
config = ConfigParser()


def Alert_error(e):

    return print("error"+e)


def CayoshiM(obj):

    print(
        "***********************[ ActionBot ]*********************************")

    try:
        data = json.loads(obj)
    except:
        Alert_error(obj)

    print(data)

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

    UserID = ''
    API_KEY = ''
    API_SECRET = ''
    ifFailed = 0

    try:  # 1
        print(Fore.RED)
        try:
            strategy_ = data['strategy']
        except:
            #
            Alert_error(Fore.YELLOW+'! non format : "strategy"  ')
        try:
            price_ = data['price']
        except:
            Alert_error(Fore.YELLOW+'! non format : "price" ')

        try:
            side_ = data['side']
        except:
            return Alert_error(Fore.RED+'! error format : "side" ')
        try:
            Type_Order = list(data['amount'])[0]
        except:
            return Alert_error(Fore.RED+'! error format : "amount":"?123" ')
        try:
            amount_in = data['amount'][1:]
        except:
            return Alert_error(Fore.RED+'! error format : "amount":"?123" ')
        try:
            symbol_in = data['symbol']
        except:
            return Alert_error(Fore.RED+'! error format : "symbol" ')
        try:
            Pass_in = data['passphrase']
        except:
            return Alert_error(Fore.RED+'! error format : "passphrase" ')

    except:
        return Alert_error('! error key format ')
# =============[ read API Connet Binace]============
 #   try:
    try:
        data_API = fu_Mysql.API_select("-", Pass_in, '-')

        if data_API != []:
            fo = data_API[0]
            fos = list(fo)
            # fos = [24, 'nateeron', 'sss56s566SSDD6s5D456SS4d65D65DSgg', 'ZXDFasdsd4dfSXDSDFasdas564FDDASXDFasdasdF', 'Hsdf45s78dfr789s8sdf',
            # 'fc20cc82-5785-5f25-9e35-058f6085a2cd', 'CROSSED', 'OFF', '', datetime.datetime(2022, 4, 18, 16, 19, 30), 'my Futuresgg', 'Future', 'stop']
    except:
        return Alert_error("Data : don't find ")
    UserID = fos[1]
    Label_API = fos[10]
    API_KEY = fos[2]
    API_SECRET = fos[3]
    line_key = fos[4]
    botAction = fos[11]
    status_ = fos[12]
    if status_ == 'stop':
        return print("Bot : stop")

    txt_error = ''
    notify = ''
    try:
        notify = LineNotify(line_key)
    except:
        txt_error = "*** LineNotify key error "
        print(txt_error)

    try:
        connect_Binace = ccxt.binance({
            'apiKey': API_KEY,
            'secret': API_SECRET,
            'enableRateLimit': True,
            'type': 'spot'
        })
    except:
        return Alert_error('! error connect_Binace : "apiKey" ')
        # ============================= จัดการเช็ก Order =================================
        # dateexp = connect_Binace.apiKey.expandtabs() #tradingAuthorityExpirationTime
        # dateexp2 = connect_Binace.fetch_balance()
        # pprint(dateexp2)
    try:
        symbol_ = connect_Binace.fetch_ticker(symbol_in)['symbol']
        order_price = connect_Binace.fetch_ticker(
            symbol_in)['last']  # ราคาเหรียญล่าสุด
        unit = symbol_.split("/")

        Crypto_me_total = connect_Binace.fetch_balance()[
            'total']  # เหรียญทั้งหมด

        # pprint(Crypto_me_total)
        Crypto_balan = connect_Binace.fetch_total_balance()[unit[0]]
        balance_Port = connect_Binace.fetch_balance(
        )['USDT']['free']  # จำนวน USDT ที่เหลือ
        Percen_price = (float(balance_Port) / 100) * \
            float(amount_in)  # ซื้อ n% ของเงินที่มี
        Percen_price_sell = connect_Binace.fetch_balance(
        )[symbol_.split('/')[0]]['free']  # .values() #['FTMUSDT']
        # pprint(Percen_price_sell)
        Percen_price_percen_sell = (
            float(Percen_price_sell) / 100) * float(amount_in)
        formatted_amount = 0.0
        if Type_Order == '@':  # ซื้อด้วยจำนวนเหรียญ FTM BTC BNB

            formatted_amount = connect_Binace.amount_to_precision(
                symbol_in,  float(amount_in))

        elif Type_Order == '$':  # ซื้อด้วยจำนวนเงิน USDT
            connect_Binace.options['createMarketBuyOrderRequiresPrice'] = False
            formatted_amount = connect_Binace.amount_to_precision(
                symbol_in,  float(amount_in) * order_price)
            # formatted_amount = connect_Binace.amount_to_precision(symbol_in,  float(amount_in) /order_price)
        elif Type_Order == '%':  # ซื้อด้วยจำนวนเงิน USDT ตาม % ที่กำหนด
            if side_ == 'buy':
                formatted_amount = connect_Binace.amount_to_precision(
                    symbol_in,  float(Percen_price) / order_price)
            else:
                formatted_amount = connect_Binace.amount_to_precision(
                    symbol_in,  float(Percen_price_percen_sell))

        amount = float(formatted_amount)
        price_Action = ''
        as_usdt = ''
        amount_Action = ''
        # ==================== ทำการซื้อ ขาย ======================================

 ###    ############################################################################[         Action Real           ]##############################################################################################################################################################################################################################################################################
        try:
            sss = connect_Binace.create_order(
                symbol_in, 'market',  side_, amount)  # , order_price
            id_Action = sss['id']
            amount_Action = sss['amount']  # จำนวนเหรียญ
            price_Action = sss['average']  # ราคาเหรียญ
            as_usdt = amount_Action * price_Action
            # user_id, apikey, botAction, price, side, amount, symbol, passphrase, strategy_name
            fu_Mysql.Alert_insert(UserID, API_KEY, botAction,
                                  price_Action, side_, amount_Action, symbol_in, Pass_in, strategy_)

        except:
            ifFailed = 1
            txt_error += '\n🛠 '+Label_API + ' Check API : Enable Spot & Margin Trading 🛠'

            notify.send('🛠 '+Label_API +
                        ' Check API : Enable Spot & Margin Trading 🛠')
            fu_Mysql.Alert_insert(UserID, API_KEY, botAction,
                                  price_Action, side_, order_price, symbol_in, Pass_in, strategy_)
            return print(txt_error)
####    ###########################################################################################################################################################################################################################################################################################################################################################################################

        if ifFailed == 0:
            balance_USDT = connect_Binace.fetch_balance()['USDT']['free']
            stiker_line = ''
            if side_ == 'buy':
                stiker_line = '🟢'
            elif side_ == 'sell':
                stiker_line = '🔴'
            price_in = ''

            if price_ != '':
                price_in = ('\nราคา Alert : {0:,} ').format(
                    float(price_)) + unit[1]
            if unit[1] == 'USDT':
                #print('Strategy Line: '+ strategy_ )
                messend = ' '+Label_API + ' '+stiker_line+' [ '+side_ + ' ' + unit[0] + ' ]\nStrategy : ' + strategy_ + '\nซื้อด้วยจำนวนเหรียญ : ' + unit[0] + price_in+(
                    '\nที่ราคา : 🛒  {0:,} ' + unit[1] + '\nจำนวนเหรียญ : ⚙️ {1:,} ' + unit[0] + '\nเป็นเงิน : 💵 {2:,.2f} '+unit[1]+'\nUSDT free = {3:,.2f}').format(price_Action, amount_Action, as_usdt, float(balance_USDT))
            else:
                messend = ' '+Label_API + ' '+stiker_line+' [ '+side_ + ' ' + unit[0] + ' ] \nStrategy : ' + strategy_ + '\nซื้อด้วยจำนวนเงิน : ' + unit[1] + price_in + (
                    '\nที่ราคา : 🛒  {0:,} ' + unit[1] + '\nจำนวนเหรียญ : ⚙️ {1:,} ' + unit[0] + '\nเป็นเงิน : 💵 {2:,} '+unit[1] + '\nUSDT free = {3:,.2f}').format(price_Action, amount_Action, as_usdt, float(balance_USDT))

            notify.send('💎'+messend)
    except:
        return Alert_error('! error connect_Binace : "apiKey" ')


def Show_All_Coins_Available(APIKEY, APISECRET):
    #print(APIKEY, APISECRET)

    try:
        connect_Binace = ccxt.binance({
            'apiKey': APIKEY,
            'secret': APISECRET,
            'enableRateLimit': True,
            'type': 'spot'
        })
    except:
        return Alert_error('! error connect_Binace : "apiKey" ')
    try:
        try:
            #sm = connect_Binace.symbols[0]

            #orderbook = connect_Binace.fetch_ticker('ETH/BTC')
            # print(orderbook)
            # bid = orderbook['bids'][0][0] if len(
            #    orderbook['bids']) > 0 else None
            # ask = orderbook['asks'][0][0] if len(
            #    orderbook['asks']) > 0 else None
            #spread = (ask - bid) if (bid and ask) else None
            # print(connect_Binace.id, 'market price', {
            #      'bid': bid, 'ask': ask, 'spread': spread})
            Crypto_me_total = ""
            Crypto_me_total2 = ""
            # Crypto_me_total = connect_Binace.fetch_balance(
            # )
            # Crypto_me_total2 = connect_Binace.fetch_balance(
            # )['info']  # เหรียญทั้งหมด ['info']['balances']
            # connect_Binace.load_markets()
            #Crypto_me_total3 = len(connect_Binace.fetch_orders('BNBUSDT'))-1
            # Crypto_me_total = connect_Binace.fetch_orders('BNBUSDT')[
            #    Crypto_me_total3]
            # Crypto_me_total = connect_Binace.fetch_tickers(
            #    ['ETH/BTC', 'BNB/USDT'])
            #fee_coin = list(Crypto_me_total)
            # print("******[close_Order]********")
            # print(orderbook)
           # pprint(close_Order)
            # pprint("******[Crypto_me_total]********")
            # while i <= len(Crypto_me_total):
            #    print(i, end=', ')
            #    i = i + 1
            # print(len(Crypto_me_total))
           # pprint(type(Crypto_me_total))
            session['DATA_TEST'] = str(
                (Crypto_me_total))
            session['DATA_TEST2'] = Crypto_me_total2
            # pprint((Crypto_me_total))
        except:
            return Alert_error('! error Crypto_me_total : "apiKey" ')
        try:
            # เหรียญที่สามารถขายได้
            Crypto_me = ''  # connect_Binace.fetch_balance()['free']

        except:
            return Alert_error('! error Crypto_me : "apiKey" ')

        lst_Val = list(Crypto_me.values())
        lst_key = list(Crypto_me.keys())
        total_USDT = 0.0
        count_lis = 0
        data_lst_key = []
        data_lst_Val = []

        try:
            for i in lst_Val:
                if float(format(i, '.4f')) > 0:

                    try:
                        info_key = str(lst_key[count_lis])

                        info_Val = format(i, ',')
                        if info_key != 'USDT':
                            data_lst_key.append(info_key + '/USDT')
                            data_lst_Val.append(info_Val)
                    except:
                        return print("error2 :" + str(total_USDT))
                count_lis = count_lis+1
            # print(data_lst_key)
            lis_inof = ''  # connect_Binace.fetch_tickers(data_lst_key)
            index = 0
            for simbo in lis_inof:
                last_price = float(lis_inof[simbo]['last'])
                val_Coin = float(data_lst_Val[index])
                value = last_price * val_Coin
                if value > 1:
                    pprint(format(value, ',.2f'))
                index += 1
            # print(data_lst_Val)
        except:
            return print("***** error for i in lst_Val*******")

        return [data_lst_key, data_lst_Val]
    except:
        return print('! error : !!! API Key  !!! Failed   !!! offline')


k = "xqd2ELJxDJr07AZibt4qgdYjmugOcQR7yTNV0erjZvLifbwvK0O9EbOwZl6hE4h5"
l = "GSXX9U6Kf25BTJhLm3KIyr8aEJpknPyig6rgOznx3ESdkIIAYFYB9FT1b12xc7C6"
#Show_All_Coins_Available(k, l)
