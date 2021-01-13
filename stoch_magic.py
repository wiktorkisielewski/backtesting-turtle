#import price
import datetime
import threading
import json
import time


eurusd_ticks = []
eurusd_sma = None
eurusd_stoch = []

audusd_ticks = []
audusd_sma = None
audusd_stoch = []

gpbusd_ticks = []
gpbusd_sma = None
gpbusd_stoch = []

usdchf_ticks = []
usdchf_sma = None
usdchf_stoch = []

euraud_ticks = []
euraud_sma = None
euraud_stoch = []

eurgpb_ticks = []
eurgpb_sma = None
eurgpb_stoch = []

x = 1618


def extraction(file, n):
    with open(file) as f:
        try:
            pre_ticks = json.load(f)
        except json.decoder.JSONDecodeError:
            f.close()
            with open(file, 'a') as f_2:
                f_2.write(']')
                f_2.close()
            with open(file) as f_3:
                pre_ticks = json.load(f_3)
        pre_ticks = pre_ticks[-n:]

    return pre_ticks


def quotes():
    global eurusd_sma, audusd_sma, gpbusd_sma, eurusd_ticks, audusd_ticks, gpbusd_ticks\
        , usdchf_sma, usdchf_ticks, euraud_sma, euraud_ticks, eurgpb_sma, eurgpb_ticks\
        , eurusd_stoch, audusd_stoch, gpbusd_stoch, usdchf_stoch, euraud_stoch, eurgpb_stoch

    eurusd_entry = None
    eurusd_exit = None
    eurusd_s = []

    audusd_entry = None
    audusd_exit = None
    audusd_s = []

    gpbusd_entry = None
    gpbusd_exit = None
    gpbusd_s = []

    usdchf_entry = None
    usdchf_exit = None
    usdchf_s = []

    euraud_entry = None
    euraud_exit = None
    euraud_s = []

    eurgpb_entry = None
    eurgpb_exit = None
    eurgpb_s = []

    inp = input('load ticks?')
    if inp == 'y':
        eurusd_ticks = extraction('ticks/eurusd_ticks.txt', x)
        audusd_ticks = extraction('ticks/audusd_ticks.txt', x)
        gpbusd_ticks = extraction('ticks/gpbusd_ticks.txt', x)
        usdchf_ticks = extraction('ticks/usdchf_ticks.txt', x)
        euraud_ticks = extraction('ticks/euraud_ticks.txt', x)
        eurgpb_ticks = extraction('ticks/eurgpb_ticks.txt', x)
        print('EURUSD:', len(eurusd_ticks), 'AUDUSD:', len(audusd_ticks), 'GPBUSD:', len(gpbusd_ticks)
            , 'USDCHF', len(usdchf_ticks), 'EURAUD', len(euraud_ticks), 'EURGPB', len(eurgpb_ticks))
    else:
        pass

    try:
        sts_t.start()
        autosave_t.start()
    except RuntimeError:
        pass

    while True:

        for eurusd_bid, eurusd_ask, audusd_bid, audusd_ask, gpbusd_bid, gpbusd_ask, usdchf_bid, usdchf_ask\
                , euraud_ask, euraud_bid, eurgpb_ask, eurgpb_bid in price.price_subscription():

            #EURUSD

            eurusd = (eurusd_bid + eurusd_ask) / 2

            eurusd_s.append(abs(eurusd_bid - eurusd_ask))
            eurusd_spread = sum(eurusd_s) / len(eurusd_s)
            if len(eurusd_s) > 1618:
                eurusd_s = eurusd_s[(len(eurusd_s) - 1618):]

            if len(eurusd_ticks) == 0:
                if eurusd != 0.0:
                    eurusd_ticks.append(eurusd)
            else:
                if (eurusd != eurusd_ticks[-1]) and ((eurusd_ticks[-1] * 1.03) > eurusd > (eurusd_ticks[-1] * 0.97)):
                    if len(eurusd_ticks) > x:
                        eurusd_sma = round((sum(eurusd_ticks) / x), 5)
                        eurusd_stoch.append(stochastic(eurusd_ticks, 100))
                        stoch = sum(eurusd_stoch[-50:]) / len(eurusd_stoch[-50:])
                        entry_s, exit_s = magic(eurusd_sma, stoch, eurusd, eurusd_spread)
                        eurusd_entry = entry_s
                        eurusd_exit = exit_s
                        if len(eurusd_stoch) >= 50:
                            eurusd_stoch = eurusd_stoch[(len(eurusd_stoch) - 50):]

                        eurusd_ticks = eurusd_ticks[(len(eurusd_ticks) - x):]
                    else:
                        eurusd_ticks.append(eurusd)
            #AUDUSD

            audusd = (audusd_bid + audusd_ask) / 2

            audusd_s.append(abs(audusd_bid - audusd_ask))
            audusd_spread = sum(audusd_s) / len(audusd_s)
            if len(audusd_s) > 1618:
                audusd_s = audusd_s[(len(audusd_s) - 1618):]

            if len(audusd_ticks) == 0:
                if audusd != 0.0:
                    audusd_ticks.append(audusd)
            else:
                if (audusd != audusd_ticks[-1]) and ((audusd_ticks[-1] * 1.03) > audusd > (audusd_ticks[-1] * 0.97)):
                    if len(audusd_ticks) > x:
                        audusd_sma = round((sum(audusd_ticks) / x), 5)
                        audusd_stoch.append(stochastic(audusd_ticks, 100))
                        stoch = sum(audusd_stoch[-50:]) / len(audusd_stoch[-50:])
                        entry_s, exit_s = magic(audusd_sma, stoch, audusd, audusd_spread)
                        audusd_entry = entry_s
                        audusd_exit = exit_s
                        if len(audusd_stoch) >= 50:
                            audusd_stoch = audusd_stoch[(len(audusd_stoch) - 50):]

                        audusd_ticks = audusd_ticks[(len(audusd_ticks) - x):]
                    else:
                        audusd_ticks.append(audusd)

            #GPBUSD

            gpbusd = (gpbusd_bid + gpbusd_ask) / 2

            gpbusd_s.append(abs(gpbusd_bid - gpbusd_ask))
            gpbusd_spread = sum(gpbusd_s) / len(gpbusd_s)
            if len(gpbusd_s) > 1618:
                gpbusd_s = gpbusd_s[(len(gpbusd_s) - 1618):]

            if len(gpbusd_ticks) == 0:
                if gpbusd != 0.0:
                    gpbusd_ticks.append(gpbusd)
            else:
                if (gpbusd != gpbusd_ticks[-1]) and ((gpbusd_ticks[-1] * 1.03) > gpbusd > (gpbusd_ticks[-1] * 0.97)):
                    if len(gpbusd_ticks) > x:
                        gpbusd_sma = round((sum(gpbusd_ticks) / x), 5)
                        gpbusd_stoch.append(stochastic(gpbusd_ticks, 100))
                        stoch = sum(gpbusd_stoch[-50:]) / len(gpbusd_stoch[-50:])
                        entry_s, exit_s = magic(gpbusd_sma, stoch, gpbusd, gpbusd_spread)
                        gpbusd_entry = entry_s
                        gpbusd_exit = exit_s
                        if len(gpbusd_stoch) >= 50:
                            gpbusd_stoch = gpbusd_stoch[(len(gpbusd_stoch) - 50):]

                        gpbusd_ticks = gpbusd_ticks[(len(gpbusd_ticks) - x):]
                    else:
                        gpbusd_ticks.append(gpbusd)

            #USDCHF

            usdchf = (usdchf_bid + usdchf_ask) / 2

            usdchf_s.append(abs(usdchf_bid - usdchf_ask))
            usdchf_spread = sum(usdchf_s) / len(usdchf_s)
            if len(usdchf_s) > 1618:
                usdchf_s = usdchf_s[(len(usdchf_s) - 1618):]

            if len(usdchf_ticks) == 0:
                if usdchf != 0.0:
                    usdchf_ticks.append(usdchf)
            else:
                if (usdchf != usdchf_ticks[-1]) and ((usdchf_ticks[-1] * 1.03) > usdchf > (usdchf_ticks[-1] * 0.97)):
                    if len(usdchf_ticks) > x:
                        usdchf_sma = round((sum(usdchf_ticks) / x), 5)
                        usdchf_stoch.append(stochastic(usdchf_ticks, 100))
                        stoch = sum(usdchf_stoch[-50:]) / len(usdchf_stoch[-50:])
                        entry_s, exit_s = magic(usdchf_sma, stoch, usdchf, usdchf_spread)
                        usdchf_entry = entry_s
                        usdchf_exit = exit_s
                        if len(usdchf_stoch) >= 50:
                            usdchf_stoch = usdchf_stoch[(len(usdchf_stoch) - 50):]

                        usdchf_ticks = usdchf_ticks[(len(usdchf_ticks) - x):]
                    else:
                        usdchf_ticks.append(usdchf)

            #EURAUD

            euraud = (euraud_bid + euraud_ask) / 2

            euraud_s.append(abs(euraud_bid - euraud_ask))
            euraud_spread = sum(euraud_s) / len(euraud_s)
            if len(euraud_s) > 1618:
                euraud_s = euraud_s[(len(euraud_s) - 1618):]

            if len(euraud_ticks) == 0:
                if euraud != 0.0:
                    euraud_ticks.append(euraud)
            else:
                if (euraud != euraud_ticks[-1]) and ((euraud_ticks[-1] * 1.03) > euraud > (euraud_ticks[-1] * 0.97)):
                    if len(euraud_ticks) > x:
                        euraud_sma = round((sum(euraud_ticks) / x), 5)
                        euraud_stoch.append(stochastic(euraud_ticks, 100))
                        stoch = sum(euraud_stoch[-50:]) / len(euraud_stoch[-50:])
                        entry_s, exit_s = magic(euraud_sma, stoch, euraud, euraud_spread)
                        euraud_entry = entry_s
                        euraud_exit = exit_s
                        if len(euraud_stoch) >= 50:
                            euraud_stoch = euraud_stoch[(len(euraud_stoch) - 50):]

                        euraud_ticks = euraud_ticks[(len(euraud_ticks) - x):]
                    else:
                        euraud_ticks.append(euraud)

            #EURGPB

            eurgpb = (eurgpb_bid + eurgpb_ask) / 2

            eurgpb_s.append(abs(eurgpb_bid - eurgpb_ask))
            eurgpb_spread = sum(eurgpb_s) / len(eurgpb_s)
            if len(eurgpb_s) > 1618:
                eurgpb_s = eurgpb_s[(len(eurgpb_s) - 1618):]

            if len(eurgpb_ticks) == 0:
                if eurgpb != 0.0:
                    eurgpb_ticks.append(eurgpb)
            else:
                if (eurgpb != eurgpb_ticks[-1]) and ((eurgpb_ticks[-1] * 1.03) > eurgpb > (eurgpb_ticks[-1] * 0.97)):
                    if len(eurgpb_ticks) > x:
                        eurgpb_sma = round((sum(eurgpb_ticks) / x), 5)
                        eurgpb_stoch.append(stochastic(eurgpb_ticks, 100))
                        stoch = sum(eurgpb_stoch[-50:]) / len(eurgpb_stoch[-50:])
                        entry_s, exit_s = magic(eurgpb_sma, stoch, eurgpb, eurgpb_spread)
                        eurgpb_entry = entry_s
                        eurgpb_exit = exit_s
                        if len(eurgpb_stoch) >= 50:
                            eurgpb_stoch = eurgpb_stoch[(len(eurgpb_stoch) - 50):]

                        eurgpb_ticks = eurgpb_ticks[(len(eurgpb_ticks) - x):]
                    else:
                        eurgpb_ticks.append(eurgpb)

            try:
                eurusd = eurusd_ticks[-1]
                audusd = audusd_ticks[-1]
                gpbusd = gpbusd_ticks[-1]
                usdchf = usdchf_ticks[-1]
                euraud = euraud_ticks[-1]
                eurgpb = eurgpb_ticks[-1]
            except IndexError:
                pass

            yield eurusd, audusd, gpbusd, usdchf, euraud, eurgpb, eurusd_entry, eurusd_exit, audusd_entry\
                , audusd_exit, gpbusd_entry, gpbusd_exit, usdchf_entry, usdchf_exit\
                , euraud_entry, euraud_exit, eurgpb_entry, eurgpb_exit, eurusd_sma, audusd_sma, gpbusd_sma, usdchf_sma\
                , euraud_sma, eurgpb_sma


def stochastic(ticks, period):
    low = min(ticks[-period:])
    high = max(ticks[-period:])
    close = ticks[-1]
    try:
        stoch = ((close - low)/(high - low)) * 100
    except ZeroDivisionError:
        stoch = 50
    return stoch


def magic(sma, stoch, price, spread):
    entry_s = None
    exit_s = None

    if spread < 0.0000625 * price:
        if (price > sma) and (5 < stoch <= 10):
            entry_s = '1'
        elif (price > sma) and (stoch <= 5):
            entry_s = '11'
        elif (price < sma) and (95 > stoch >= 90):
            entry_s = '2'
        elif (price < sma) and (stoch >= 95):
            entry_s = '22'

    if stoch >= 80:
        exit_s = '1'

    if stoch <= 20:
        exit_s = '2'

    return entry_s, exit_s


def key():
    while True:
        inp = input()
        if inp == 'save':
            save_the_ticks()
        if inp == 'ticks':
            print('EURUSD:', len(eurusd_ticks), 'AUDUSD:', len(audusd_ticks), 'GPBUSD:', len(gpbusd_ticks)
                  , 'USDCHF', len(usdchf_ticks), 'EURAUD', len(euraud_ticks), 'EURGPB', len(eurgpb_ticks))
        if inp == 'show':
            print('what instrument?')
            inp2 = input()
            if inp2 == 'eurusd':
                try:
                    print('MAX', max(eurusd_ticks), 'MIN', min(eurusd_ticks), 'AVG', sum(eurusd_ticks)/len(eurusd_ticks)
                          , 'LAST', eurusd_ticks[-1], 'SMA', eurusd_sma, 'STOCH', eurusd_stoch[-1])
                except IndexError:
                    print('MAX', max(eurusd_ticks), 'MIN', min(eurusd_ticks), 'AVG',
                          sum(eurusd_ticks) / len(eurusd_ticks), 'LAST', eurusd_ticks[-1])
            if inp2 == 'audusd':
                try:
                    print('MAX', max(audusd_ticks), 'MIN', min(audusd_ticks), 'AVG',
                          sum(audusd_ticks) / len(audusd_ticks)
                          , 'LAST', audusd_ticks[-1], 'SMA', audusd_sma, 'STOCH', audusd_stoch[-1])
                except IndexError:
                    print('MAX', max(audusd_ticks), 'MIN', min(audusd_ticks), 'AVG',
                          sum(audusd_ticks) / len(audusd_ticks), 'LAST', audusd_ticks[-1])
            if inp2 == 'gpbusd':
                try:
                    print('MAX', max(gpbusd_ticks), 'MIN', min(gpbusd_ticks), 'AVG',
                          sum(gpbusd_ticks) / len(gpbusd_ticks)
                          , 'LAST', gpbusd_ticks[-1], 'SMA', gpbusd_sma, 'STOCH', gpbusd_stoch[-1])
                except IndexError:
                    print('MAX', max(gpbusd_ticks), 'MIN', min(gpbusd_ticks), 'AVG',
                          sum(gpbusd_ticks) / len(gpbusd_ticks), 'LAST', gpbusd_ticks[-1])
            if inp2 == 'usdchf':
                try:
                    print('MAX', max(usdchf_ticks), 'MIN', min(usdchf_ticks), 'AVG',
                          sum(usdchf_ticks) / len(usdchf_ticks)
                          , 'LAST', usdchf_ticks[-1], 'SMA', usdchf_sma, 'STOCH', usdchf_stoch[-1])
                except IndexError:
                    print('MAX', max(usdchf_ticks), 'MIN', min(usdchf_ticks), 'AVG',
                          sum(usdchf_ticks) / len(usdchf_ticks), 'LAST', usdchf_ticks[-1])
            if inp2 == 'euraud':
                try:
                    print('MAX', max(euraud_ticks), 'MIN', min(euraud_ticks), 'AVG', sum(euraud_ticks)/len(euraud_ticks)
                          , 'LAST', euraud_ticks[-1], 'SMA', euraud_sma, 'STOCH', euraud_stoch[-1])
                except IndexError:
                    print('MAX', max(euraud_ticks), 'MIN', min(euraud_ticks), 'AVG',
                          sum(euraud_ticks) / len(euraud_ticks), 'LAST', euraud_ticks[-1])
            if inp2 == 'eurgpb':
                try:
                    print('MAX', max(eurgpb_ticks), 'MIN', min(eurgpb_ticks), 'AVG', sum(eurgpb_ticks)/len(eurgpb_ticks)
                          , 'LAST', eurgpb_ticks[-1], 'SMA', eurgpb_sma, 'STOCH', eurgpb_stoch[-1])
                except IndexError:
                    print('MAX', max(eurgpb_ticks), 'MIN', min(eurgpb_ticks), 'AVG',
                          sum(eurgpb_ticks) / len(eurgpb_ticks), 'LAST', eurgpb_ticks[-1])
        if inp == 'reset':
            print('what instrument?')
            inp2 = input()
            if inp2 == 'eurusd':
                del eurusd_ticks[:]
                revival('ticks/eurusd_ticks.txt')
            if inp2 == 'audusd':
                del audusd_ticks[:]
                revival('ticks/audusd_ticks.txt')
            if inp2 == 'gpbusd':
                del gpbusd_ticks[:]
                revival('ticks/gpbusd_ticks.txt')
            if inp2 == 'usdchf':
                del usdchf_ticks[:]
                revival('ticks/usdchf_ticks.txt')
            if inp2 == 'euraud':
                del euraud_ticks[:]
                revival('ticks/euraud_ticks.txt')
            if inp2 == 'eurgpb':
                del eurgpb_ticks[:]
                revival('ticks/eurgpb_ticks.txt')
        if inp == 'show stoch':
            print('what instrument?')
            inp2 = input()
            if inp2 == 'eurusd':
                print(eurusd_stoch[-100:])
            if inp2 == 'audusd':
                print(audusd_stoch[-100:])
            if inp2 == 'gpbusd':
                print(gpbusd_stoch[-100:])
            if inp2 == 'usdchf':
                print(usdchf_stoch[-100:])
            if inp2 == 'euraud':
                print(euraud_stoch[-100:])
            if inp2 == 'eurgpb':
                print(eurgpb_stoch[-100:])


def save_the_ticks():
    print('### SAVING... ###')
    with open('ticks/eurusd_ticks.txt', 'w') as f_eurusd:
        json.dump(eurusd_ticks, f_eurusd)
        f_eurusd.close()
    with open('ticks/audusd_ticks.txt', 'w') as f_audusd:
        json.dump(audusd_ticks, f_audusd)
        f_audusd.close()
    with open('ticks/gpbusd_ticks.txt', 'w') as f_gpbusd:
        json.dump(gpbusd_ticks, f_gpbusd)
        f_gpbusd.close()
    with open('ticks/usdchf_ticks.txt', 'w') as f_usdchf:
        json.dump(usdchf_ticks, f_usdchf)
        f_usdchf.close()
    with open('ticks/euraud_ticks.txt', 'w') as f_euraud:
        json.dump(euraud_ticks, f_euraud)
        f_euraud.close()
    with open('ticks/eurgpb_ticks.txt', 'w') as f_eurgpb:
        json.dump(eurgpb_ticks, f_eurgpb)
        f_eurgpb.close()
    print('### TICKS SAVED ### {} ###'.format(datetime.datetime.now()))


def revival(path):
    inp = input('input price')
    ticks = [float(inp)]
    with open(path, 'w') as f:
        json.dump(ticks, f)
        f.close()


def auto_save():
    while True:
        time.sleep(300)
        save_the_ticks()


quotes_t = threading.Thread(target=quotes)
sts_t = threading.Thread(target=key)
autosave_t = threading.Thread(target=auto_save)


quotes_t.start()

