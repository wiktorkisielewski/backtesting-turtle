from simplefix import FixMessage, FixParser
from trade import send_msg
import range_master
import alert
import auth
import socket
import datetime
import threading
import time
import json


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((auth.SocketConnectHost, auth.Q_SocketConnectPort))

parser = FixParser()

n = 1


def logon():
    global n
    message = FixMessage()

    message.append_pair(8, "FIX.4.4")
    message.append_pair(35, "A")
    message.append_pair(34, n)
    message.append_pair(49, auth.SenderCompID)
    message.append_utc_timestamp(52)
    message.append_pair(56, auth.TargetCompID)
    message.append_pair(57, 'QUOTE')
    message.append_pair(98, "0")
    message.append_pair(141, "Y")
    message.append_pair(108, "30")
    message.append_pair(553, auth.Username)
    message.append_pair(554, auth.Password)

    parser.append_buffer(message.encode())
    sent = parser.get_message()
    print("logon2 request ", sent)

    s.sendall(message.encode())
    response = s.recv(5201)

    parser.append_buffer(response)
    out = parser.get_message()
    print("logon response2", out)
    n += 1


def heartbeat_msg():
    global n
    heartbeat = FixMessage()

    heartbeat.append_pair(8, "FIX.4.4")
    heartbeat.append_pair(35, "0")
    heartbeat.append_pair(34, n)
    heartbeat.append_pair(49, auth.SenderCompID)
    heartbeat.append_utc_timestamp(52)
    heartbeat.append_pair(56, auth.TargetCompID)
    heartbeat.append_pair(57, "QUOTE")
    n += 1

    try:
        s.sendall(heartbeat.encode())
    except BrokenPipeError:
        print('PRICE DiSCONETED')
        range_master.save_the_ticks()
        alert.send_alert('PRICE CONNECTION LOST')


def data_subscribe(sub, instr, x):
    global n
    data = FixMessage()

    data.append_pair(8, "FIX.4.4")
    data.append_pair(35, "V")
    data.append_pair(49, auth.SenderCompID)
    data.append_pair(56, auth.TargetCompID)
    data.append_pair(34, n)
    data.append_utc_timestamp(52)
    data.append_pair(262, "2")
    data.append_pair(263, sub)
    data.append_pair(264, "1")
    data.append_pair(265, "1") #1
    data.append_pair(146, "1")
    data.append_pair(55, instr)
    data.append_pair(267, "2")
    data.append_pair(269, "0")
    data.append_pair(269, "1")

    sent = data.encode()

    s.sendall(data.encode())
    out = str(s.recv(auth.Q_SocketConnectPort))
    n += 1

    if x is False:
        #print("data request ", str(sent).replace('\\x01', '|'))
        #print("data response", out.replace('\\x01', '|'))
        pass
    else:
        return out


switch = False
d = datetime.datetime.now()

eurusd_prev = 0
eurusd_bid = 0
eurusd_ask = 0

audusd_prev = 0
audusd_bid = 0
audusd_ask = 0

gbpusd_prev = 0
gbpusd_bid = 0
gbpusd_ask = 0

usdchf_prev = 0
usdchf_bid = 0
usdchf_ask = 0

euraud_prev = 0
euraud_bid = 0
euraud_ask = 0

usdjpy_prev = 0
usdjpy_bid = 0
usdjpy_ask = 0


def keep_beating():
    time.sleep(25)
    while True:
        global d, n
        heartbeat_msg()
        n += 1
        time.sleep(25)
        d = datetime.datetime.now()


def extract_quotes(out):

    bid_index = out.find('269=0')
    if bid_index != -1:
        bid_price = (((out[bid_index + 13:bid_index + 20])).replace('\\', '')).replace('x', '')

        ask_index = out.find('269=1')
        ask_price = (((out[ask_index + 13:ask_index + 20])).replace('\\', '')).replace('x', '')

        if len(bid_price) > len(ask_price):
            ask_price = ask_price + ('0' * (len(bid_price) - len(ask_price)))
        elif len(ask_price) > len(bid_price):
            bid_price = bid_price + ('0' * (len(ask_price) - len(bid_price)))

        try:
            ask_price = float((ask_price.replace(' ', '')))
            bid_price = float((bid_price.replace(' ', '')))
        except ValueError:
            print('VALUE ERROR', out)

        px = (ask_price + bid_price) / 2

        return px, ask_price, bid_price


def price_subscription():
    global n, switch
    if switch is False:
        switch = True
        logon()
        print("gathering market data...")
        data_subscribe('1', '1', False)
        data_subscribe('1', '5', False)
        data_subscribe('1', '2', False)
        data_subscribe('1', '6', False)
        data_subscribe('1', '14', False)
        data_subscribe('1', '4', False)
        try:
            t_2.start()
            t_q.start()
            t_qc.start()
        except RuntimeError:
            pass
    else:
        pass
    global eurusd_prev, audusd_prev, gbpusd_prev, usdchf_prev, euraud_prev, usdjpy_prev

    while True:
        if eurusd_prev != eurusd_bid:
            eurusd_prev = eurusd_bid
        if audusd_prev != audusd_bid:
            audusd_prev = audusd_bid
        if gbpusd_prev != gbpusd_bid:
            gbpusd_prev = gbpusd_bid
        if usdchf_prev != usdchf_bid:
            usdchf_prev = usdchf_bid
        if euraud_prev != euraud_bid:
            euraud_prev = euraud_bid
        if usdjpy_prev != usdjpy_bid:
            usdjpy_prev = usdjpy_bid
        yield eurusd_bid, eurusd_ask, audusd_bid, audusd_ask, gbpusd_bid, gbpusd_ask \
            , usdchf_bid, usdchf_ask, euraud_ask, euraud_bid, usdjpy_ask, usdjpy_bid


def extraction(file, symbol):
    with open(file) as f:
        try:
            pre_ticks = json.load(f)
            tick = pre_ticks[-1]
        except json.decoder.JSONDecodeError:
            f.close()
            with open(file, 'a') as f_2:
                f_2.write(']')
                f_2.close()
            with open(file) as f_3:
                try:
                    pre_ticks = json.load(f_3)
                    tick = pre_ticks[-1]
                except json.decoder.JSONDecodeError:
                    alert.send_alert('JSON ERROR')
                    if symbol == "1":
                        tick = eurusd_prev
                    elif symbol == "5":
                        tick = audusd_prev
                    elif symbol == "2":
                        tick = gbpusd_prev
                    elif symbol == "6":
                        tick = usdchf_prev
                    elif symbol == "14":
                        tick = euraud_prev
                    elif symbol == "4":
                        tick = usdjpy_prev

        return tick


def q():
    global eurusd_bid, eurusd_ask, eurusd_prev, audusd_bid, audusd_ask, audusd_prev, gbpusd_bid, gbpusd_ask\
        , gbpusd_prev, euraud_ask, euraud_bid, usdjpy_ask, usdjpy_bid\
        , usdchf_bid, usdchf_ask, usdchf_prev, euraud_prev, usdjpy_prev

    eurusd_prev = extraction('ticks/eurusd_ticks.txt', '1')
    print('eurusd', eurusd_prev)
    audusd_prev = extraction('ticks/audusd_ticks.txt', '5')
    print('audusd', audusd_prev)
    gbpusd_prev = extraction('ticks/gbpusd_ticks.txt', '2')
    print('gbpusd', gbpusd_prev)
    usdchf_prev = extraction('ticks/usdchf_ticks.txt', '6')
    print('usdchf', usdchf_prev)
    euraud_prev = extraction('ticks/euraud_ticks.txt', '14')
    print('euraud', euraud_prev)
    usdjpy_prev = extraction('ticks/usdjpy_ticks.txt', '4')
    print('usdjpy', usdjpy_prev)

    while True:
        out = str(s.recv(auth.Q_SocketConnectPort))

        try:
            px, ask_price, bid_price = extract_quotes(out)

            if (eurusd_prev * 1.0003) > px > (eurusd_prev * 0.9997):
                eurusd_ask = ask_price
                eurusd_bid = bid_price
            if (audusd_prev * 1.0003) > px > (audusd_prev * 0.9997):
                audusd_ask = ask_price
                audusd_bid = bid_price
            if (gbpusd_prev * 1.0003) > px > (gbpusd_prev * 0.9997):
                gbpusd_ask = ask_price
                gbpusd_bid = bid_price
            if (usdchf_prev * 1.0003) > px > (usdchf_prev * 0.9997):
                usdchf_ask = ask_price
                usdchf_bid = bid_price
            if (euraud_prev * 1.0003) > px > (euraud_prev * 0.9997):
                euraud_ask = ask_price
                euraud_bid = bid_price
            if (usdjpy_prev * 1.0003) > px > (usdjpy_prev * 0.9997):
                usdjpy_ask = ask_price
                usdjpy_bid = bid_price
        except TypeError:
            pass


def revival(symbol, p_px, path):
    data_subscribe('2', symbol, False)
    time.sleep(1)
    try:
        px, bid_price, ask_price = extract_quotes(data_subscribe('1', symbol, True))
        if (p_px * 1.01) > px > (p_px * 0.99):
            ask = ask_price
            bid = bid_price
            return ask, bid
        else:
            return extraction(path, symbol), extraction(path, symbol)
    except TypeError:
        return extraction(path, symbol), extraction(path, symbol)


def quote_check():
    global eurusd_bid, eurusd_ask, eurusd_prev, audusd_bid, audusd_ask, audusd_prev, gbpusd_bid, gbpusd_ask \
        , gbpusd_prev, euraud_ask, euraud_bid, usdjpy_ask, usdjpy_bid \
        , usdchf_bid, usdchf_ask, usdchf_prev, euraud_prev, usdjpy_prev

    while True:
        eurusd_p = eurusd_bid
        audusd_p = audusd_bid
        gbpusd_p = gbpusd_bid
        usdchf_p = usdchf_bid
        euraud_p = euraud_bid
        usdjpy_p = usdjpy_bid
        time.sleep(60)
        if (eurusd_p == eurusd_bid) or (eurusd_bid == 0) or (eurusd_ask == 0):
            eurusd_bid, eurusd_ask = revival('1', eurusd_p, 'ticks/eurusd_ticks.txt')
        if (audusd_p == audusd_bid) or (audusd_bid == 0) or (audusd_ask == 0):
            audusd_bid, audusd_ask = revival('5', audusd_p, 'ticks/audusd_ticks.txt')
        if (gbpusd_p == gbpusd_bid) or (gbpusd_bid == 0) or (gbpusd_ask == 0):
            gbpusd_bid, gbpusd_ask = revival('2', gbpusd_p, 'ticks/gbpusd_ticks.txt')
        if (usdchf_p == usdchf_bid) or (usdchf_bid == 0) or (usdchf_ask == 0):
            usdchf_bid, usdchf_ask = revival('6', usdchf_p, 'ticks/usdchf_ticks.txt')
        if (euraud_p == euraud_bid) or (euraud_bid == 0) or (euraud_ask == 0):
            euraud_bid, euraud_ask = revival('14', euraud_p, 'ticks/euraud_ticks.txt')
        if (usdjpy_p == usdjpy_bid) or (usdjpy_bid == 0) or (usdjpy_ask == 0):
            usdjpy_bid, usdjpy_ask = revival('9', usdjpy_p, 'ticks/usdjpy_ticks.txt')


t_1 = threading.Thread(target=price_subscription)
t_2 = threading.Thread(target=keep_beating)

t_q = threading.Thread(target=q)
t_qc = threading.Thread(target=quote_check)

t_1.start()
