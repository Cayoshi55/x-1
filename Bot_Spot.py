from array import array
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
    Label_API = fos[10]
    API_KEY = fos[2]
    API_SECRET = fos[3]
    line_key = fos[4]


#   if Bot_RUNTEST == 'on':
#       notify = LineNotify(LineNotify_Test)
#   elif Bot_RUNTEST == 'off':
#       notify = LineNotify(line_key)
#
#   # ============== Chack passphrase ===============
#   if Pass_in != password_config:
#       pprint('')
#       print(
#           Fore.RED+'==============================[ ! error  ]=================================')
#       print(Fore.RED+'! error passphrase :  don''t match')
#       print(Fore.RED+'! error file *.ini : File Name is PassPhrase')
#       return 'passphrase : dont match '
#
#   else:
#
#       try:
#           connect_Binace = ccxt.binance({
#               'apiKey': API_KEY,
#               'secret': API_SECRET,
#               'enableRateLimit': True,
#               'type': 'spot'
#           })
#           # ============================= จัดการเช็ก Order =================================
#           # dateexp = connect_Binace.apiKey.expandtabs() #tradingAuthorityExpirationTime
#           #dateexp2 = connect_Binace.fetch_balance()
#           # pprint(dateexp2)
#           symbol_ = connect_Binace.fetch_ticker(symbol_in)['symbol']
#           order_price = connect_Binace.fetch_ticker(
#               symbol_in)['last']  # ราคาเหรียญล่าสุด
#           unit = symbol_.split("/")
#
#           Crypto_me_total = connect_Binace.fetch_balance()[
#               'total']  # เหรียญทั้งหมด
#
#           # pprint(Crypto_me_total)
#           Crypto_balan = connect_Binace.fetch_total_balance()[unit[0]]
#           balance_Port = connect_Binace.fetch_balance(
#           )['USDT']['free']  # จำนวน USDT ที่เหลือ
#           Percen_price = (float(balance_Port) / 100) * \
#               float(amount_in)  # ซื้อ n% ของเงินที่มี
#           Percen_price_sell = connect_Binace.fetch_balance(
#           )[symbol_.split('/')[0]]['free']  # .values() #['FTMUSDT']
#           # pprint(Percen_price_sell)
#           Percen_price_percen_sell = (
#               float(Percen_price_sell) / 100) * float(amount_in)
#           formatted_amount = 0.0
#           if Type_Order == '@':  # ซื้อด้วยจำนวนเหรียญ FTM BTC BNB
#
#               formatted_amount = connect_Binace.amount_to_precision(
#                   symbol_in,  float(amount_in))
#
#           elif Type_Order == '$':  # ซื้อด้วยจำนวนเงิน USDT
#               connect_Binace.options['createMarketBuyOrderRequiresPrice'] = False
#               formatted_amount = connect_Binace.amount_to_precision(
#                   symbol_in,  float(amount_in) * order_price)
#               #formatted_amount = connect_Binace.amount_to_precision(symbol_in,  float(amount_in) /order_price)
#           elif Type_Order == '%':  # ซื้อด้วยจำนวนเงิน USDT ตาม % ที่กำหนด
#               if side_ == 'buy':
#                   formatted_amount = connect_Binace.amount_to_precision(
#                       symbol_in,  float(Percen_price) / order_price)
#               else:
#                   formatted_amount = connect_Binace.amount_to_precision(
#                       symbol_in,  float(Percen_price_percen_sell))
#
#           amount = float(formatted_amount)
#           color_line = Fore.WHITE
#           color_ = Fore.WHITE
#           try:  # ==================== ทำการซื้อ ขาย ======================================
#
#               if side_ == 'sell':
#                   color_ = Fore.RED
#                   color_line = Fore.MAGENTA
#               elif side_ == 'buy':
#                   color_ = Fore.GREEN
#                   color_line = Fore.GREEN
#
#               price_Action = ''
#               as_usdt = ''
#               amount_Action = ''
#
#               if Bot_RUNTEST == 'off' and side_ != '':
#
#                   ###############################################################################[         Action Real           ]##############################################################################################################################################################################################################################################################################
#                   try:
#                       sss = connect_Binace.create_order(
#                           symbol_in, 'market',  side_, amount)  # , order_price
#                       id_Action = sss['id']
#                       amount_Action = sss['amount']  # จำนวนเหรียญ
#                       price_Action = sss['average']  # ราคาเหรียญ
#                       as_usdt = amount_Action * price_Action
#                   except:
#                       ifFailed = 1
#                       print(Fore.RED+'==================[ '+Fore.YELLOW + Label_API +
#                             ' | '+color_ + side_ + Fore.RED+' : Failed ]=====================')
#                       print(Fore.RED+Pass_in +
#                             ' Check API : Enable Spot & Margin Trading')
#                       notify.send(
#                           '🛠 '+Pass_in+' Check API : Enable Spot & Margin Trading 🛠')
################################################################################################################################################################################################################################################################################################################################################################################################
#
#               elif Bot_RUNTEST == 'on' and side_ != '':
#                   amount_Action = amount
#                   price_Action = order_price
#                   as_usdt = amount * order_price
#
#               format_buy = ''
#               if unit[1] == 'USDT':
#                   format_buy = '{0:,.2f}'
#               else:
#                   format_buy = '{0:,}'
#
#               if Print_Short_Line == 'on' and side_ != '' and ifFailed == 0:
#
#                   print(Fore.CYAN + 'By : '+Fore.YELLOW + Label_API)
#                   print(Fore.CYAN + 'Strategy : ' + Fore.YELLOW+strategy_+Fore.CYAN+' | Action : ' + color_ + side_ + Fore.YELLOW + ' ' + symbol_+Fore.CYAN+' | ' + ('Price : '+Fore.YELLOW+'{0:,} ').format(
#                       price_Action) + Fore.CYAN+' | '+Fore.CYAN + ('money : '+Fore.YELLOW + format_buy + Fore.CYAN+' ' + unit[1]).format(as_usdt)+' | '+Fore.CYAN + ('Number of coins : '+Fore.YELLOW+'{0:,} '+Fore.CYAN + unit[0]).format(amount_Action))
#
#               elif Print_Short_Line == 'off' and side_ != '' and ifFailed == 0:
#
#                   print(Fore.CYAN + 'By : '+Fore.YELLOW + Label_API)
#                   print(Fore.CYAN + 'Strategy : ' + Fore.YELLOW+strategy_)
#                   print(Fore.CYAN + 'Action : ' + color_ +
#                         side_ + Fore.YELLOW + ' ' + symbol_)
#                   print(Fore.CYAN + ('Price : '+Fore.YELLOW +
#                         '{0:,} ').format(price_Action))
#                   print(Fore.CYAN + ('money : '+Fore.YELLOW+format_buy +
#                         Fore.CYAN + ' ' + unit[1]).format(as_usdt))
#                   print(Fore.CYAN + ('Number of coins : '+Fore.YELLOW +
#                         '{0:,} '+Fore.CYAN + unit[0]).format(amount_Action))
#
#                   # -------------------------------------------------
#                   # เมื่อ เกิด Alert ให้เก็บข้อมูลลง DATA
#                   #fu_Mysql.Alert_insert(userID, apikey, botAction, price,side, amount, symbol, passphrase, strategy_name)
#           # ======================== ถ้าไม่สำเร็จ ให้ แจ้ง =================================================
#           except:
#               if ifFailed == 0:
#                   print(Fore.RED+'==================[ '+Fore.YELLOW + Label_API +
#                         ' | '+color_ + side_ + Fore.RED+' : Failed ]=====================')
#               amount_s = amount * order_price  # เงินจาก tradingview สั่งซื้อน้อย
#
#               if amount_s < 10:
#                   print(Fore.CYAN + 'Order low money USDT < 10 ')
#                   print('USDT : {0:,.2f}'.format(amount_s))
#               if balance_Port < amount_s and side_ == 'buy':
#                   print(Fore.CYAN + 'Low Balance Port USDT  ')
#                   print('USDT Balance : {0:,.2f}'.format(balance_Port))
#               if Crypto_balan < amount and side_ == 'sell':
#                   print(Fore.CYAN + 'Number of coins ' +
#                         unit[0] + ' not enough to sell')
#                   print(unit[0] + ' have : {0:,}'.format(Crypto_balan))
#                   print('Want to sell : {0:,}'.format(amount))
#
#               print(
#                   Fore.RED+'===================================================================================')
#
#           else:  # ถ้าซื้อสำเร็จ ให้ส่ง Line =================================================
#
#               # ===============================================[ Line ]===============================================================
#               if ifFailed == 0:
#                   balance_USDT = connect_Binace.fetch_balance()[
#                       'USDT']['free']
#                   stiker_line = ''
#                   if side_ == 'buy':
#                       stiker_line = '🟢'
#                   elif side_ == 'sell':
#                       stiker_line = '🔴'
#                   price_in = ''
#                   txt_test = ''
#                   if Bot_RUNTEST == 'on':
#                       txt_test = ('\n🛠🛠🛠[ Running TEST ]🛠🛠🛠')
#                   if price_ != '':
#                       price_in = ('\nราคา Alert : {0:,} ').format(
#                           float(price_)) + unit[1]
#                   if unit[1] == 'USDT':
#                       #print('Strategy Line: '+ strategy_ )
#                       messend = ' '+Label_API + ' '+stiker_line+' [ '+side_ + ' ' + unit[0] + ' ]'+txt_test+'\nStrategy : ' + strategy_ + '\nซื้อด้วยจำนวนเหรียญ : ' + unit[0] + price_in+(
#                           '\nที่ราคา : 🛒  {0:,} ' + unit[1] + '\nจำนวนเหรียญ : ⚙️ {1:,} ' + unit[0] + '\nเป็นเงิน : 💵 {2:,.2f} '+unit[1]+'\nUSDT free = {3:,.2f}').format(price_Action, amount_Action, as_usdt, float(balance_USDT))
#                   else:
#                       messend = ' '+Label_API + ' '+stiker_line+' [ '+side_ + ' ' + unit[0] + ' ]'+txt_test+'\nStrategy : ' + strategy_ + '\nซื้อด้วยจำนวนเงิน : ' + unit[1] + price_in + (
#                           '\nที่ราคา : 🛒  {0:,} ' + unit[1] + '\nจำนวนเหรียญ : ⚙️ {1:,} ' + unit[0] + '\nเป็นเงิน : 💵 {2:,} '+unit[1] + '\nUSDT free = {3:,.2f}').format(price_Action, amount_Action, as_usdt, float(balance_USDT))
#                   if Send_line == 'on':
#                       notify.send('💎'+messend)
#
#                   messend_2 = ''
#                   total_value = 0.0
#                   if Show_All_Coins_Available == 'on':
#                       # เหรียญที่สามารถขายได้
#                       Crypto_me = connect_Binace.fetch_balance()['free']
#                       lst_Val = list(Crypto_me.values())
#                       lst_key = list(Crypto_me.keys())
#                       # pprint(Crypto_me)
#                       # M pass1166 = 'USDT': 4.48853108,
#                       # P 553399G
#                       total_USDT = 0.0
#                       count_lis = 0
#                       print(Fore.CYAN+'========================[ All Coins value > '+str(
#                           Coins_value)+' USDT ]========================')
#                       for i in lst_Val:
#                           if float(i) > 0:
#                               try:
#                                   symbol_f = str(lst_key[count_lis]) + 'USDT'
#                                   #print(Fore.YELLOW+symbol_f+Fore.MAGENTA +' | '+ str(connect_Binace.fetch_ticker(symbol_f)['last']) )
#                                   # print(Fore.YELLOW+'============================================================================='+Fore.MAGENTA)
#
#                                   #print(Fore.CYAN+ connect_Binace.fetch_ticker( 'FTMUSDT' )+Fore.MAGENTA)
#                                   ppp = float(
#                                       connect_Binace.fetch_ticker(symbol_f)['last'])
#                                   #print(Fore.YELLOW+'('+str(ppp) +'x'+str(i)+') = '+str(ppp * i) +Fore.MAGENTA)
#                                   total_value = ppp * i
#                                   #print(Fore.YELLOW+'22222 ============================================================================='+Fore.MAGENTA)
#                               except:
#                                   total_value = i
#                               #print(str(total_value)+' > '+ str(Coins_value))
#                               if total_value > Coins_value:
#                                   #print(Fore.YELLOW+'11111 ============================================================================='+Fore.MAGENTA)
#                                   messend_2 = messend_2 + ((str(lst_key[count_lis]) + ' : {0:,} ').format(
#                                       i) + ('Total : {0:,.2f}').format(total_value) + ' USDT \n')
#                                   #print(Fore.YELLOW+'0000 ============================================================================='+Fore.MAGENTA)
#                                   print((Fore.CYAN + lst_key[count_lis] + ' : ' + Fore.GREEN + '{0:,} ').format(i) + (
#                                       Fore.CYAN + 'Total : '+Fore.GREEN+'{0:,.2f}').format(total_value) + Fore.CYAN + ' USDT')
#                                   total_USDT = total_USDT+total_value
#                                   #print(Fore.YELLOW+'22222 ============================================================================='+Fore.MAGENTA)
#                           count_lis = count_lis+1
#                       sum_usdt = 'Total USDT = ' + \
#                           str('{0:,.2f}').format(total_USDT)
#                       print('Total USDT = '+Fore.YELLOW +
#                             str('{0:,.2f}').format(total_USDT))
#
#                       if Send_line == 'on':
#                           notify.send(
#                               ' เหรียญ Crypto ทั้งหมดที่มี \n'+messend_2 + '\n'+sum_usdt)
#                       print(
#                           Fore.CYAN + '============================================================================')
#               else:
#                   return {'Failed': 'Failed'}
#           return {'Action': 'Succeed'}
#       except:
#           # print(ifFailed)
#           if API_error_Send_line == 'on':
#               # if ifFailed == 0:
#               #notify.send('🛠 Check API : Enable Spot & Margin Trading 🛠')
#               # else:
#               #notify.send('💥 🔥! error : API Key !Failed 🔥💥')
#               notify.send('💥 🔥'+Label_API + ' '+Pass_in +
#                           ' ! error : API Key !Failed 🔥💥')
#           print(
#               Fore.RED + '===========================================================================')
#           print('! error : !!! API Key  !!! Failed   !!! offline')
#           return {'! error': 'API Key !Failed'}
#   return ""
