import numpy as np
from stoch_magic import extraction, stochastic
import matplotlib.pyplot as plt
import datetime


file = ['eurgbp', 'euraud', 'eurusd', 'gbpusd', 'usdchf', 'audusd']
#month = ['09_2007', '03_2008', '08_2011', '10_2013', '12_2014', '04_2016', '03_2020']
overall_profit = 1000
overall = []


def plot_it():
    def moving_av():
        dist = 5000
        ma = [None] * dist
        i = dist
        while i < len(y):
            ma_v = sum(y[(i - dist):i]) / dist
            i += 1
            ma.append(ma_v)

        return ma

    m = 0
    while m <= 5:
        def backtest():
            global overall_profit
            capital = [1000] * 5000
            cash = 1000
            trades = 0
            good = 0
            bad = 0
            period = 500
            z = 5000
            ticks = y
            in_long = False
            in_short = False
            long_entry = None
            short_entry = None
            ma = moving_av()
            while z < len(ticks):
                profit = 0
                if ma[z] < ticks[z] < min(y[(z - period):z]) and in_long is False and in_short is False:
                    in_long = True
                    trades += 1
                    long_entry = ticks[z]
                if in_long is True:
                    if ticks[z] > max(y[(z - period):z]) or ticks[z] < long_entry * 0.99:
                        if (ticks[z] - long_entry) != 0:
                            profit += 1000 * ((ticks[z] - long_entry) / ticks[z])
                            in_long = False
                            cash += profit
                        elif (ticks[z] - long_entry) == 0:
                            in_long = False
                            cash += profit

                if ma[z] > ticks[z] > max(y[(z - period):z])and in_short is False and in_long is False:
                    in_short = True
                    trades += 1
                    short_entry = ticks[z]
                if in_short is True:
                    if ticks[z] < min(y[(z - period):z]) or ticks[z] > short_entry * 1.01:
                        if (short_entry - ticks[z]) != 0:
                            profit += 1000 * ((short_entry - ticks[z]) / ticks[z])
                            in_short = False
                            cash += profit
                        if (short_entry - ticks[z]) == 0:
                            in_short = False
                            cash += profit

                if profit > 0:
                    good += 1
                elif profit <= 0:
                    bad += 1

                capital.append(cash)
                z += 1

            return capital, trades, good, bad

        i = 1
        while i <= 1:
            try:
                y = extraction('backtesting/16_20/' + file[m] + '/ ' + str(i) + '.txt', 100000000)
                y = y[::1]
                fig, axs = plt.subplots(2)
                fig.suptitle(file[m] + '  ' + str(len(y)))
                axs[0].plot(y, linewidth=0.3)
                axs[0].plot(moving_av(), linewidth=0.2)
                fig.set_figwidth(15)

                capital, trades, good, bad = backtest()
                axs[1].plot(capital, linewidth=0.3)

                try:
                    print(overall[-1])
                    overall.append(overall[-1] + (capital[-1] - 1000))
                    axs[3].plot(overall, linewidth=0.5)
                except IndexError:
                    pass

                plt.savefig(file[m] + '_plot.png', dpi=300)
                plt.close()

                if trades != 0:
                    commisions = trades * 0.08
                    print(file[m], 'GAIN: ', capital[-1] - 1000, 'TRADES: ', trades, 'NET PROFIT', (capital[-1] - 1000) - commisions, 'ACC', good / trades, datetime.datetime.now())
                i += 1
            except FileNotFoundError:
                i += 1
        m += 1

plot_it()

