import trade
import range_master
import threading
import time
import datetime
import json

eurusd = audusd = gbpusd = usdchf = euraud = usdjpy = 0

eurusd_entry = eurusd_exit = audusd_entry = audusd_exit = gbpusd_entry = gbpusd_exit \
    = usdchf_entry = usdchf_exit = euraud_entry = euraud_exit = usdjpy_entry = usdjpy_exit = None

eurusd_timer = audusd_timer = gbpusd_timer = usdchf_timer = euraud_timer = usdjpy_timer = 0
timer = 180

eurusd_stop_price = audusd_stop_price = gbpusd_stop_price = usdchf_stop_price = euraud_stop_price = usdjpy_stop_price\
    = eurusd_open_price = audusd_open_price = gbpusd_open_price = usdchf_open_price = euraud_open_price\
    = usdjpy_open_price = None

eurusd_long = eurusd_short = audusd_long = audusd_short = gbpusd_long = gbpusd_short \
    = usdchf_long = usdchf_short = euraud_long = euraud_short = usdjpy_long = usdjpy_short = 0

trades = [['eurusd', None, None], ['audusd', None, None], ['gbpusd', None, None], ['usdchf', None, None], ['euraud', None, None], ['usdjpy', None, None]]

eurusd_symbol = '1'
eurusd_arr = 0
eurusd_open_tick = 0

audusd_symbol = '5'
audusd_arr = 1
audusd_open_tick = 0

gbpusd_symbol = '2'
gbpusd_arr = 2
gbpusd_open_tick = 0

usdchf_symbol = '6'
usdchf_arr = 3
usdchf_open_tick = 0

euraud_symbol = '14'
euraud_arr = 4
euraud_open_tick = 0

usdjpy_symbol = '4'
usdjpy_arr = 5
usdjpy_open_tick = 0

size_f = 1000
risk_f = 0.01
tick_stop = 28800 / (range_master.noise_cancelation + 1)


def hrtbt():
    while True:
        global d
        trade.heartbeat_msg()
        time.sleep(25)


def main():
    global eurusd, audusd, gbpusd, usdchf, euraud, usdjpy, eurusd_entry, eurusd_exit, audusd_entry\
            , audusd_exit, gbpusd_entry, gbpusd_exit, usdchf_entry, usdchf_exit, euraud_entry, euraud_exit\
            , usdjpy_entry, usdjpy_exit
    is_on = False
    for eurusd, audusd, gbpusd, usdchf, euraud, usdjpy, eurusd_entry, eurusd_exit, audusd_entry\
            , audusd_exit, gbpusd_entry, gbpusd_exit, usdchf_entry, usdchf_exit, euraud_entry, euraud_exit\
            , usdjpy_entry, usdjpy_exit in range_master.quotes():

        eurusd, audusd, gbpusd, usdchf, euraud, usdjpy, eurusd_entry, eurusd_exit, audusd_entry\
            , audusd_exit, gbpusd_entry, gbpusd_exit, usdchf_entry, usdchf_exit, euraud_entry, euraud_exit\
            , usdjpy_entry, usdjpy_exit = eurusd, audusd, gbpusd, usdchf, euraud, usdjpy, eurusd_entry, eurusd_exit, audusd_entry\
            , audusd_exit, gbpusd_entry, gbpusd_exit, usdchf_entry, usdchf_exit, euraud_entry, euraud_exit\
            , usdjpy_entry, usdjpy_exit

        if is_on is not True:
            is_on = True
            print("{}".format('INITAIALIZING'), end="\r")
            trade.login()
            hrtbt_t.start()
            eurusd_main.start()
            print('EURUSD ON')
            audusd_main.start()
            print('AUDUSD ON')
            gbpusd_main.start()
            print('GBPUSD ON')
            usdchf_main.start()
            print('USDCHF ON')
            euraud_main.start()
            print('EURAUD ON')
            usdjpy_main.start()
            print('USDJPY ON')
            inp = input('load trades?')
            if inp == 'y':
                load_trades()
            else:
                save_trades()
        else:
            pass


def open_pos(direction, size, sym):
    sent = trade.market_order(direction, size, sym)
    return sent


def eurusd_main():
    global eurusd_timer, eurusd_stop_price, eurusd_open_price, eurusd_entry, eurusd_exit, eurusd_long, eurusd_short, eurusd_open_tick

    eurusd_last = 0

    while True:
        if eurusd_last != eurusd:
            eurusd_last = eurusd
            if eurusd_short == 0 and eurusd_long == 0:
                if eurusd_entry == '1':
                    sent = open_pos('1', size_f, eurusd_symbol)
                    if sent == 1:
                        eurusd_open_price = round(float(eurusd), 5)
                        eurusd_stop_price = round(float((eurusd_open_price - (eurusd_open_price * risk_f))), 5)
                        print('OPEN', eurusd_open_price, 'STOP', eurusd_stop_price, 'ENTRY', eurusd_entry, 'EXIT', eurusd_exit)
                        eurusd_open_tick = 0
                        eurusd_long += 1
                        trades[eurusd_arr][1] = 'long'
                        trades[eurusd_arr][2] = str(eurusd_stop_price)
                        save_trades()
                elif eurusd_entry == '2':
                    sent = open_pos('2', size_f, eurusd_symbol)
                    if sent == 1:
                        eurusd_open_price = round(float(eurusd), 5)
                        eurusd_stop_price = round(float((eurusd_open_price + (eurusd_open_price * risk_f))), 5)
                        print('OPEN', eurusd_open_price, 'STOP', eurusd_stop_price, 'ENTRY', eurusd_entry, 'EXIT', eurusd_exit)
                        eurusd_open_tick = 0
                        eurusd_short += 1
                        trades[eurusd_arr][1] = 'short'
                        trades[eurusd_arr][2] = str(eurusd_stop_price)
                        save_trades()

            else:
                eurusd_open_tick += 1
                if eurusd_long != 0:
                    if eurusd_exit == '1':
                            sent = open_pos('2', (eurusd_long * size_f), eurusd_symbol)
                            if sent == 1:
                                print('eurusd closed at {}'.format(eurusd))
                                eurusd_long = 0
                                trades[eurusd_arr][1] = None
                                trades[eurusd_arr][2] = None
                                save_trades()
                    elif eurusd_open_tick >= tick_stop:
                        sent = open_pos('2', (eurusd_long * size_f), eurusd_symbol)
                        if sent == 1:
                            print('eurusd T_STOP at {}'.format(eurusd))
                            eurusd_long = 0
                            trades[eurusd_arr][1] = None
                            trades[eurusd_arr][2] = None
                            save_trades()
                    else:
                        try:
                            if eurusd_stop_price > eurusd:
                                sent = open_pos('2', (eurusd_long * size_f), eurusd_symbol)
                                if sent == 1:
                                    print('eurusd P_STOP at {}'.format(eurusd))
                                    eurusd_long = 0
                                    trades[eurusd_arr][1] = None
                                    trades[eurusd_arr][2] = None
                                    save_trades()
                        except TypeError:
                            pass

                elif eurusd_short != 0:
                    if eurusd_exit == '2':
                            sent = open_pos('1', (eurusd_short * size_f), eurusd_symbol)
                            if sent == 1:
                                print('eurusd closed at {}'.format(eurusd))
                                eurusd_short = 0
                                trades[eurusd_arr][1] = None
                                trades[eurusd_arr][2] = None
                                save_trades()
                    elif eurusd_open_tick >= tick_stop:
                        sent = open_pos('1', (eurusd_short * size_f), eurusd_symbol)
                        if sent == 1:
                            print('eurusd T_STOP at {}'.format(eurusd))
                            eurusd_short = 0
                            trades[eurusd_arr][1] = None
                            trades[eurusd_arr][2] = None
                            save_trades()
                    else:
                        try:
                            if eurusd_stop_price < eurusd:
                                sent = open_pos('1', (eurusd_short * size_f), eurusd_symbol)
                                if sent == 1:
                                    print('eurusd P_STOP at {}'.format(eurusd))
                                    eurusd_short = 0
                                    trades[eurusd_arr][1] = None
                                    trades[eurusd_arr][2] = None
                                    save_trades()
                        except TypeError:
                            pass
        eurusd_entry = eurusd_entry = None


def audusd_main():
    global audusd_timer, audusd_stop_price, audusd_open_price, audusd_entry, audusd_exit, audusd_long, audusd_short, audusd_open_tick

    audusd_last = 0

    while True:
        if audusd_last != audusd:
            audusd_last = audusd
            if audusd_short == 0 and audusd_long == 0:
                if audusd_entry == '1':
                    sent = open_pos('1', size_f, audusd_symbol)
                    if sent == 1:
                        audusd_open_price = round(float(audusd), 5)
                        audusd_stop_price = round(float((audusd_open_price - (audusd_open_price * risk_f))), 5)
                        print('OPEN', audusd_open_price, 'STOP', audusd_stop_price, 'ENTRY', audusd_entry, 'EXIT', audusd_exit)
                        audusd_open_tick = 0
                        audusd_long += 1
                        trades[audusd_arr][1] = 'long'
                        trades[audusd_arr][2] = str(audusd_stop_price)
                        save_trades()
                elif audusd_entry == '2':
                    sent = open_pos('2', size_f, audusd_symbol)
                    if sent == 1:
                        audusd_open_price = round(float(audusd), 5)
                        audusd_stop_price = round(float((audusd_open_price + (audusd_open_price * risk_f))), 5)
                        print('OPEN', audusd_open_price, 'STOP', audusd_stop_price, 'ENTRY', audusd_entry, 'EXIT', audusd_exit)
                        audusd_open_tick = 0
                        audusd_short += 1
                        trades[audusd_arr][1] = 'short'
                        trades[audusd_arr][2] = str(audusd_stop_price)
                        save_trades()

            else:
                audusd_open_tick += 1
                if audusd_long != 0:
                    if audusd_exit == '1':
                            sent = open_pos('2', (audusd_long * size_f), audusd_symbol)
                            if sent == 1:
                                print('audusd closed at {}'.format(audusd))
                                audusd_long = 0
                                trades[audusd_arr][1] = None
                                trades[audusd_arr][2] = None
                                save_trades()
                    elif audusd_open_tick >= tick_stop:
                        sent = open_pos('2', (audusd_long * size_f), audusd_symbol)
                        if sent == 1:
                            print('audusd T_STOP at {}'.format(audusd))
                            audusd_long = 0
                            trades[audusd_arr][1] = None
                            trades[audusd_arr][2] = None
                            save_trades()
                    else:
                        try:
                            if audusd_stop_price > audusd:
                                sent = open_pos('2', (audusd_long * size_f), audusd_symbol)
                                if sent == 1:
                                    print('audusd P_STOP at {}'.format(audusd))
                                    audusd_long = 0
                                    trades[audusd_arr][1] = None
                                    trades[audusd_arr][2] = None
                                    save_trades()
                        except TypeError:
                            pass

                elif audusd_short != 0:
                    if audusd_exit == '2':
                            sent = open_pos('1', (audusd_short * size_f), audusd_symbol)
                            if sent == 1:
                                print('audusd closed at {}'.format(audusd))
                                audusd_short = 0
                                trades[audusd_arr][1] = None
                                trades[audusd_arr][2] = None
                                save_trades()
                    elif audusd_open_tick >= tick_stop:
                        sent = open_pos('1', (audusd_short * size_f), audusd_symbol)
                        if sent == 1:
                            print('audusd T_STOP at {}'.format(audusd))
                            audusd_short = 0
                            trades[audusd_arr][1] = None
                            trades[audusd_arr][2] = None
                            save_trades()
                    else:
                        try:
                            if audusd_stop_price < audusd:
                                sent = open_pos('1', (audusd_short * size_f), audusd_symbol)
                                if sent == 1:
                                    print('audusd P_STOP at {}'.format(audusd))
                                    audusd_short = 0
                                    trades[audusd_arr][1] = None
                                    trades[audusd_arr][2] = None
                                    save_trades()
                        except TypeError:
                            pass
        audusd_entry = audusd_entry = None


def gbpusd_main():
    global gbpusd_timer, gbpusd_stop_price, gbpusd_open_price, gbpusd_entry, gbpusd_exit, gbpusd_long, gbpusd_short, gbpusd_open_tick

    gbpusd_last = 0

    while True:
        if gbpusd_last != gbpusd:
            gbpusd_last = gbpusd
            if gbpusd_short == 0 and gbpusd_long == 0:
                if gbpusd_entry == '1':
                    sent = open_pos('1', size_f, gbpusd_symbol)
                    if sent == 1:
                        gbpusd_open_price = round(float(gbpusd), 5)
                        gbpusd_stop_price = round(float((gbpusd_open_price - (gbpusd_open_price * risk_f))), 5)
                        print('OPEN', gbpusd_open_price, 'STOP', gbpusd_stop_price, 'ENTRY', gbpusd_entry, 'EXIT', gbpusd_exit)
                        gbpusd_open_tick = 0
                        gbpusd_long += 1
                        trades[gbpusd_arr][1] = 'long'
                        trades[gbpusd_arr][2] = str(gbpusd_stop_price)
                        save_trades()
                elif gbpusd_entry == '2':
                    sent = open_pos('2', size_f, gbpusd_symbol)
                    if sent == 1:
                        gbpusd_open_price = round(float(gbpusd), 5)
                        gbpusd_stop_price = round(float((gbpusd_open_price + (gbpusd_open_price * risk_f))), 5)
                        print('OPEN', gbpusd_open_price, 'STOP', gbpusd_stop_price, 'ENTRY', gbpusd_entry, 'EXIT', gbpusd_exit)
                        gbpusd_open_tick = 0
                        gbpusd_short += 1
                        trades[gbpusd_arr][1] = 'short'
                        trades[gbpusd_arr][2] = str(gbpusd_stop_price)
                        save_trades()

            else:
                gbpusd_open_tick += 1
                if gbpusd_long != 0:
                    if gbpusd_exit == '1':
                            sent = open_pos('2', (gbpusd_long * size_f), gbpusd_symbol)
                            if sent == 1:
                                print('gbpusd closed at {}'.format(gbpusd))
                                gbpusd_long = 0
                                trades[gbpusd_arr][1] = None
                                trades[gbpusd_arr][2] = None
                                save_trades()
                    elif gbpusd_open_tick >= tick_stop:
                        sent = open_pos('2', (gbpusd_long * size_f), gbpusd_symbol)
                        if sent == 1:
                            print('gbpusd T_STOP at {}'.format(gbpusd))
                            gbpusd_long = 0
                            trades[gbpusd_arr][1] = None
                            trades[gbpusd_arr][2] = None
                            save_trades()
                    else:
                        try:
                            if gbpusd_stop_price > gbpusd:
                                sent = open_pos('2', (gbpusd_long * size_f), gbpusd_symbol)
                                if sent == 1:
                                    print('gbpusd P_STOP at {}'.format(gbpusd))
                                    gbpusd_long = 0
                                    trades[gbpusd_arr][1] = None
                                    trades[gbpusd_arr][2] = None
                                    save_trades()
                        except TypeError:
                            pass

                elif gbpusd_short != 0:
                    if gbpusd_exit == '2':
                            sent = open_pos('1', (gbpusd_short * size_f), gbpusd_symbol)
                            if sent == 1:
                                print('gbpusd closed at {}'.format(gbpusd))
                                gbpusd_short = 0
                                trades[gbpusd_arr][1] = None
                                trades[gbpusd_arr][2] = None
                                save_trades()
                    elif gbpusd_open_tick >= tick_stop:
                        sent = open_pos('1', (gbpusd_short * size_f), gbpusd_symbol)
                        if sent == 1:
                            print('gbpusd T_STOP at {}'.format(gbpusd))
                            gbpusd_short = 0
                            trades[gbpusd_arr][1] = None
                            trades[gbpusd_arr][2] = None
                            save_trades()
                    else:
                        try:
                            if gbpusd_stop_price < gbpusd:
                                sent = open_pos('1', (gbpusd_short * size_f), gbpusd_symbol)
                                if sent == 1:
                                    print('gbpusd P_STOP at {}'.format(gbpusd))
                                    gbpusd_short = 0
                                    trades[gbpusd_arr][1] = None
                                    trades[gbpusd_arr][2] = None
                                    save_trades()
                        except TypeError:
                            pass
        gbpusd_entry = gbpusd_entry = None


def usdchf_main():
    global usdchf_timer, usdchf_stop_price, usdchf_open_price, usdchf_entry, usdchf_exit, usdchf_long, usdchf_short, usdchf_open_tick

    usdchf_last = 0

    while True:
        if usdchf_last != usdchf:
            usdchf_last = usdchf
            if usdchf_short == 0 and usdchf_long == 0:
                if usdchf_entry == '1':
                    sent = open_pos('1', size_f, usdchf_symbol)
                    if sent == 1:
                        usdchf_open_price = round(float(usdchf), 5)
                        usdchf_stop_price = round(float((usdchf_open_price - (usdchf_open_price * risk_f))), 5)
                        print('OPEN', usdchf_open_price, 'STOP', usdchf_stop_price, 'ENTRY', usdchf_entry, 'EXIT', usdchf_exit)
                        usdchf_open_tick = 0
                        usdchf_long += 1
                        trades[usdchf_arr][1] = 'long'
                        trades[usdchf_arr][2] = str(usdchf_stop_price)
                        save_trades()
                elif usdchf_entry == '2':
                    sent = open_pos('2', size_f, usdchf_symbol)
                    if sent == 1:
                        usdchf_open_price = round(float(usdchf), 5)
                        usdchf_stop_price = round(float((usdchf_open_price + (usdchf_open_price * risk_f))), 5)
                        print('OPEN', usdchf_open_price, 'STOP', usdchf_stop_price, 'ENTRY', usdchf_entry, 'EXIT', usdchf_exit)
                        usdchf_open_tick = 0
                        usdchf_short += 1
                        trades[usdchf_arr][1] = 'short'
                        trades[usdchf_arr][2] = str(usdchf_stop_price)
                        save_trades()

            else:
                usdchf_open_tick += 1
                if usdchf_long != 0:
                    if usdchf_exit == '1':
                            sent = open_pos('2', (usdchf_long * size_f), usdchf_symbol)
                            if sent == 1:
                                print('usdchf closed at {}'.format(usdchf))
                                usdchf_long = 0
                                trades[usdchf_arr][1] = None
                                trades[usdchf_arr][2] = None
                                save_trades()
                    elif usdchf_open_tick >= tick_stop:
                        sent = open_pos('2', (usdchf_long * size_f), usdchf_symbol)
                        if sent == 1:
                            print('usdchf T_STOP at {}'.format(usdchf))
                            usdchf_long = 0
                            trades[usdchf_arr][1] = None
                            trades[usdchf_arr][2] = None
                            save_trades()
                    else:
                        try:
                            if usdchf_stop_price > usdchf:
                                sent = open_pos('2', (usdchf_long * size_f), usdchf_symbol)
                                if sent == 1:
                                    print('usdchf P_STOP at {}'.format(usdchf))
                                    usdchf_long = 0
                                    trades[usdchf_arr][1] = None
                                    trades[usdchf_arr][2] = None
                                    save_trades()
                        except TypeError:
                            pass

                elif usdchf_short != 0:
                    if usdchf_exit == '2':
                            sent = open_pos('1', (usdchf_short * size_f), usdchf_symbol)
                            if sent == 1:
                                print('usdchf closed at {}'.format(usdchf))
                                usdchf_short = 0
                                trades[usdchf_arr][1] = None
                                trades[usdchf_arr][2] = None
                                save_trades()
                    elif usdchf_open_tick >= tick_stop:
                        sent = open_pos('1', (usdchf_short * size_f), usdchf_symbol)
                        if sent == 1:
                            print('usdchf T_STOP at {}'.format(usdchf))
                            usdchf_short = 0
                            trades[usdchf_arr][1] = None
                            trades[usdchf_arr][2] = None
                            save_trades()
                    else:
                        try:
                            if usdchf_stop_price < usdchf:
                                sent = open_pos('1', (usdchf_short * size_f), usdchf_symbol)
                                if sent == 1:
                                    print('usdchf P_STOP at {}'.format(usdchf))
                                    usdchf_short = 0
                                    trades[usdchf_arr][1] = None
                                    trades[usdchf_arr][2] = None
                                    save_trades()
                        except TypeError:
                            pass
        usdchf_entry = usdchf_entry = None


def euraud_main():
    global euraud_timer, euraud_stop_price, euraud_open_price, euraud_entry, euraud_exit, euraud_long, euraud_short, euraud_open_tick

    euraud_last = 0

    while True:
        if euraud_last != euraud:
            euraud_last = euraud
            if euraud_short == 0 and euraud_long == 0:
                if euraud_entry == '1':
                    sent = open_pos('1', size_f, euraud_symbol)
                    if sent == 1:
                        euraud_open_price = round(float(euraud), 5)
                        euraud_stop_price = round(float((euraud_open_price - (euraud_open_price * risk_f))), 5)
                        print('OPEN', euraud_open_price, 'STOP', euraud_stop_price, 'ENTRY', euraud_entry, 'EXIT', euraud_exit)
                        euraud_open_tick = 0
                        euraud_long += 1
                        trades[euraud_arr][1] = 'long'
                        trades[euraud_arr][2] = str(euraud_stop_price)
                        save_trades()
                elif euraud_entry == '2':
                    sent = open_pos('2', size_f, euraud_symbol)
                    if sent == 1:
                        euraud_open_price = round(float(euraud), 5)
                        euraud_stop_price = round(float((euraud_open_price + (euraud_open_price * risk_f))), 5)
                        print('OPEN', euraud_open_price, 'STOP', euraud_stop_price, 'ENTRY', euraud_entry, 'EXIT', euraud_exit)
                        euraud_open_tick = 0
                        euraud_short += 1
                        trades[euraud_arr][1] = 'short'
                        trades[euraud_arr][2] = str(euraud_stop_price)
                        save_trades()

            else:
                euraud_open_tick += 1
                if euraud_long != 0:
                    if euraud_exit == '1':
                            sent = open_pos('2', (euraud_long * size_f), euraud_symbol)
                            if sent == 1:
                                print('euraud closed at {}'.format(euraud))
                                euraud_long = 0
                                trades[euraud_arr][1] = None
                                trades[euraud_arr][2] = None
                                save_trades()
                    elif euraud_open_tick >= tick_stop:
                        sent = open_pos('2', (euraud_long * size_f), euraud_symbol)
                        if sent == 1:
                            print('euraud T_STOP at {}'.format(euraud))
                            euraud_long = 0
                            trades[euraud_arr][1] = None
                            trades[euraud_arr][2] = None
                            save_trades()
                    else:
                        try:
                            if euraud_stop_price > euraud:
                                sent = open_pos('2', (euraud_long * size_f), euraud_symbol)
                                if sent == 1:
                                    print('euraud P_STOP at {}'.format(euraud))
                                    euraud_long = 0
                                    trades[euraud_arr][1] = None
                                    trades[euraud_arr][2] = None
                                    save_trades()
                        except TypeError:
                            pass

                elif euraud_short != 0:
                    if euraud_exit == '2':
                            sent = open_pos('1', (euraud_short * size_f), euraud_symbol)
                            if sent == 1:
                                print('euraud closed at {}'.format(euraud))
                                euraud_short = 0
                                trades[euraud_arr][1] = None
                                trades[euraud_arr][2] = None
                                save_trades()
                    elif euraud_open_tick >= tick_stop:
                        sent = open_pos('1', (euraud_short * size_f), euraud_symbol)
                        if sent == 1:
                            print('euraud T_STOP at {}'.format(euraud))
                            euraud_short = 0
                            trades[euraud_arr][1] = None
                            trades[euraud_arr][2] = None
                            save_trades()
                    else:
                        try:
                            if euraud_stop_price < euraud:
                                sent = open_pos('1', (euraud_short * size_f), euraud_symbol)
                                if sent == 1:
                                    print('euraud P_STOP at {}'.format(euraud))
                                    euraud_short = 0
                                    trades[euraud_arr][1] = None
                                    trades[euraud_arr][2] = None
                                    save_trades()
                        except TypeError:
                            pass
        euraud_entry = euraud_entry = None


def usdjpy_main():
    global usdjpy_timer, usdjpy_stop_price, usdjpy_open_price, usdjpy_entry, usdjpy_exit, usdjpy_long, usdjpy_short, usdjpy_open_tick

    usdjpy_last = 0

    while True:
        if usdjpy_last != usdjpy:
            usdjpy_last = usdjpy
            if usdjpy_short == 0 and usdjpy_long == 0:
                if usdjpy_entry == '1':
                    sent = open_pos('1', size_f, usdjpy_symbol)
                    if sent == 1:
                        usdjpy_open_price = round(float(usdjpy), 5)
                        usdjpy_stop_price = round(float((usdjpy_open_price - (usdjpy_open_price * risk_f))), 5)
                        print('OPEN', usdjpy_open_price, 'STOP', usdjpy_stop_price, 'ENTRY', usdjpy_entry, 'EXIT', usdjpy_exit)
                        usdjpy_open_tick = 0
                        usdjpy_long += 1
                        trades[usdjpy_arr][1] = 'long'
                        trades[usdjpy_arr][2] = str(usdjpy_stop_price)
                        save_trades()
                elif usdjpy_entry == '2':
                    sent = open_pos('2', size_f, usdjpy_symbol)
                    if sent == 1:
                        usdjpy_open_price = round(float(usdjpy), 5)
                        usdjpy_stop_price = round(float((usdjpy_open_price + (usdjpy_open_price * risk_f))), 5)
                        print('OPEN', usdjpy_open_price, 'STOP', usdjpy_stop_price, 'ENTRY', usdjpy_entry, 'EXIT', usdjpy_exit)
                        usdjpy_open_tick = 0
                        usdjpy_short += 1
                        trades[usdjpy_arr][1] = 'short'
                        trades[usdjpy_arr][2] = str(usdjpy_stop_price)
                        save_trades()

            else:
                usdjpy_open_tick += 1
                if usdjpy_long != 0:
                    if usdjpy_exit == '1':
                            sent = open_pos('2', (usdjpy_long * size_f), usdjpy_symbol)
                            if sent == 1:
                                print('usdjpy closed at {}'.format(usdjpy))
                                usdjpy_long = 0
                                trades[usdjpy_arr][1] = None
                                trades[usdjpy_arr][2] = None
                                save_trades()
                    elif usdjpy_open_tick >= tick_stop:
                        sent = open_pos('2', (usdjpy_long * size_f), usdjpy_symbol)
                        if sent == 1:
                            print('usdjpy T_STOP at {}'.format(usdjpy))
                            usdjpy_long = 0
                            trades[usdjpy_arr][1] = None
                            trades[usdjpy_arr][2] = None
                            save_trades()
                    else:
                        try:
                            if usdjpy_stop_price > usdjpy:
                                sent = open_pos('2', (usdjpy_long * size_f), usdjpy_symbol)
                                if sent == 1:
                                    print('usdjpy P_STOP at {}'.format(usdjpy))
                                    usdjpy_long = 0
                                    trades[usdjpy_arr][1] = None
                                    trades[usdjpy_arr][2] = None
                                    save_trades()
                        except TypeError:
                            pass

                elif usdjpy_short != 0:
                    if usdjpy_exit == '2':
                            sent = open_pos('1', (usdjpy_short * size_f), usdjpy_symbol)
                            if sent == 1:
                                print('usdjpy closed at {}'.format(usdjpy))
                                usdjpy_short = 0
                                trades[usdjpy_arr][1] = None
                                trades[usdjpy_arr][2] = None
                                save_trades()
                    elif usdjpy_open_tick >= tick_stop:
                        sent = open_pos('1', (usdjpy_short * size_f), usdjpy_symbol)
                        if sent == 1:
                            print('usdjpy T_STOP at {}'.format(usdjpy))
                            usdjpy_short = 0
                            trades[usdjpy_arr][1] = None
                            trades[usdjpy_arr][2] = None
                            save_trades()
                    else:
                        try:
                            if usdjpy_stop_price < usdjpy:
                                sent = open_pos('1', (usdjpy_short * size_f), usdjpy_symbol)
                                if sent == 1:
                                    print('usdjpy P_STOP at {}'.format(usdjpy))
                                    usdjpy_short = 0
                                    trades[usdjpy_arr][1] = None
                                    trades[usdjpy_arr][2] = None
                                    save_trades()
                        except TypeError:
                            pass
        usdjpy_entry = usdjpy_entry = None


def save_trades():
    with open('trades.txt', 'w') as trades_f:
        json.dump(trades, trades_f)
        trades_f.close()
    print(trades, datetime.datetime.now())


def load_trades():
    global trades, eurusd_long, eurusd_short, audusd_long, audusd_short, gbpusd_long, gbpusd_short\
        , usdchf_long, usdchf_short, euraud_long, euraud_short, usdjpy_long, usdjpy_short\
        , eurusd_stop_price, audusd_stop_price, gbpusd_stop_price, usdchf_stop_price\
        , euraud_stop_price, usdjpy_stop_price

    try:
        with open('trades.txt', 'r') as trades_f:
            trades = json.load(trades_f)
            print(trades)
    except FileNotFoundError:
        print('no trades file')

    if trades[0][1] == 'long':
        eurusd_long = 1
        eurusd_stop_price = float(trades[0][2])
    elif trades[0][1] == 'double long':
        eurusd_long = 2
        eurusd_stop_price = float(trades[0][2])
    elif trades[0][1] == 'short':
        eurusd_short = 1
        eurusd_stop_price = float(trades[0][2])
    elif trades[0][1] == 'double short':
        eurusd_short = 2
        eurusd_stop_price = float(trades[0][2])

    if trades[1][1] == 'long':
        audusd_long = 1
        audusd_stop_price = float(trades[1][2])
    elif trades[1][1] == 'double long':
        audusd_long = 2
        audusd_stop_price = float(trades[1][2])
    elif trades[1][1] == 'short':
        audusd_short = 1
        audusd_stop_price = float(trades[1][2])
    elif trades[1][1] == 'double short':
        audusd_short = 2
        audusd_stop_price = float(trades[1][2])

    if trades[2][1] == 'long':
        gbpusd_long = 1
        gbpusd_stop_price = float(trades[2][2])
    elif trades[2][1] == 'double long':
        gbpusd_long = 2
        gbpusd_stop_price = float(trades[2][2])
    elif trades[2][1] == 'short':
        gbpusd_short = 1
        gbpusd_stop_price = float(trades[2][2])
    elif trades[2][1] == 'double short':
        gbpusd_short = 2
        gbpusd_stop_price = float(trades[2][2])

    if trades[3][1] == 'long':
        usdchf_long = 1
        usdchf_stop_price = float(trades[3][2])
    elif trades[3][1] == 'double long':
        usdchf_long = 2
        usdchf_stop_price = float(trades[3][2])
    elif trades[3][1] == 'short':
        usdchf_short = 1
        usdchf_stop_price = float(trades[3][2])
    elif trades[3][1] == 'double short':
        usdchf_short = 2
        usdchf_stop_price = float(trades[3][2])

    if trades[4][1] == 'long':
        euraud_long = 1
        euraud_stop_price = float(trades[4][2])
    elif trades[4][1] == 'double long':
        euraud_long = 2
        euraud_stop_price = float(trades[4][2])
    elif trades[4][1] == 'short':
        euraud_short = 1
        euraud_stop_price = float(trades[4][2])
    elif trades[4][1] == 'double short':
        euraud_short = 2
        euraud_stop_price = float(trades[4][2])

    if trades[5][1] == 'long':
        usdjpy_long = 1
        usdjpy_stop_price = float(trades[5][2])
    elif trades[5][1] == 'double long':
        usdjpy_long = 2
        usdjpy_stop_price = float(trades[5][2])
    elif trades[5][1] == 'short':
        usdjpy_short = 1
        usdjpy_stop_price = float(trades[5][2])
    elif trades[5][1] == 'double short':
        usdjpy_short = 2
        usdjpy_stop_price = float(trades[5][2])

    print('EURUSD', eurusd_long, eurusd_short, eurusd_stop_price
          , 'AUDUSD', audusd_long, audusd_short, audusd_stop_price
          , 'GPBUSD', gbpusd_long, gbpusd_short, gbpusd_stop_price
          , 'USDCHF', usdchf_long, usdchf_short, usdchf_stop_price
          , 'EURAUD', euraud_long, euraud_short, euraud_stop_price
          , 'USDJPY', usdjpy_long, usdjpy_short, usdjpy_stop_price)


hrtbt_t = threading.Thread(target=hrtbt)
eurusd_main = threading.Thread(target=eurusd_main)
audusd_main = threading.Thread(target=audusd_main)
gbpusd_main = threading.Thread(target=gbpusd_main)
usdchf_main = threading.Thread(target=usdchf_main)
euraud_main = threading.Thread(target=euraud_main)
usdjpy_main = threading.Thread(target=usdjpy_main)


main()
