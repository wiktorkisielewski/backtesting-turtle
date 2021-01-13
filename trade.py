from simplefix import FixMessage, FixParser
import auth
import alert
import socket
import datetime
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((auth.SocketConnectHost, auth.T_SocketConnectPort))

parser = FixParser()

n = 1
socket_open = False


def reset_n():
    global n
    n = 1


def login():
    global n
    message = FixMessage()

    print('UTC', datetime.datetime.utcnow())
    print('LOCAL', datetime.datetime.now())

    message.append_pair(8, "FIX.4.4")
    message.append_pair(35, "A")
    message.append_pair(34, n)
    message.append_pair(49, auth.SenderCompID)
    message.append_utc_timestamp(52)
    message.append_pair(56, auth.TargetCompID)
    message.append_pair(57, 'TRADE')
    message.append_pair(98, "0")
    message.append_pair(141, "Y")
    message.append_pair(108, "30")
    message.append_pair(553, auth.Username)
    message.append_pair(554, auth.Password)

    msg = message.encode()
    print("logon msg", msg)

    try:
        s.send(msg)
    except BrokenPipeError:
        time.sleep(2.5)
        s.send(msg)

    print("logon response", s.recv(7550))
    n += 1


def send_msg(order_msg):
    global socket_open, n
    while True:
        if socket_open is True:
            time.sleep(1)
        elif socket_open is False:
            socket_open = True
            s.send(order_msg)
            n += 1
            response = s.recv(auth.T_SocketConnectPort)
            #print(str(response).replace('\\x01', '|'))
            socket_open = False
            break
    return response


def market_order(side, qty, symbol):
    order = FixMessage()
    sent = 0

    order.append_pair(8, "FIX.4.4")
    order.append_pair(35, "D")
    order.append_pair(49, auth.SenderCompID)
    order.append_pair(56, auth.TargetCompID)
    order.append_pair(34, n)
    order.append_utc_timestamp(52)
    order.append_pair(50, 'order')
    order.append_pair(57, 'TRADE')
    order.append_utc_timestamp(11)
    order.append_pair(55, symbol)
    order.append_pair(54, side)
    order.append_pair(59, "3")
    order.append_utc_timestamp(60)
    order.append_pair(40, "1")
    order.append_pair(38, qty)

    # print("sent order", str(order.encode()).replace('\\x01', '|'))

    try:
        response = send_msg(order.encode())
        sent += 1
    except BrokenPipeError:
        print('ORDER ERROR')
        alert.send_alert('ORDER CONNECTION LOST')

    return sent


def heartbeat_msg():
    heartbeat = FixMessage()

    heartbeat.append_pair(8, "FIX.4.4")
    heartbeat.append_pair(35, "0")
    heartbeat.append_pair(34, n)
    heartbeat.append_pair(49, auth.SenderCompID)
    heartbeat.append_utc_timestamp(52)
    heartbeat.append_pair(56, auth.TargetCompID)
    heartbeat.append_pair(57, "TRADES")

    parser.append_buffer(heartbeat.encode())

    try:
        send_msg(heartbeat.encode())
    except BrokenPipeError:
        print('T D')
        #range_master.save_the_ticks()
        alert.send_alert('TRADE CONNECTION LOST')
        #n = 1
        #login()
