# backtesting_turtle
Backtesting engine - allows to see how well a trading strategy would have performed on historical data. </br></br>
This example is based on Richard Denis's strategy from 80's </br>
(The trade is initiated on a new 40-day high. The exit signal is a close below the 20-day low.)

## Technologies used:
* python3.7
* numpy
* matplotlib

## run
Execute turtle.py file, while in repo directory:

```
python3 turtle.py
```
## input
Historical data is stored in a .txt file and imported as a python list, it contains prices of various currency pairs.</br>
Sample input:
```
[1.2345, 1.4567, 1.8901, 1.2345, ... , 1.6789]
```

## output
The program returns simulation results:
```
eurgbp GAIN:  32.49470611786023 TRADES:  597 NET PROFIT -15.265293882139765 ACC 0.6532663316582915 2021-01-13 13:09:20.330729
```
It produces a .png file with 2 charts. Upper one is a visualization of price changes, the bootom one is capital curve

![Alt text](https://github.com/wiktorkisielewski/backtesting-turtle/blob/main/eurgbp_plot.png "Optional Title")
