"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch

Copyright 2018, Georgia Institute of Technology (Georgia Tech)
Atlanta, Georgia 30332
All Rights Reserved

Template code for CS 4646/7646

Georgia Tech asserts copyright ownership of this template and all derivative
works, including solutions to the projects assigned in this course. Students
and other users of this template code are advised not to share it with others
or to make it available on publicly viewable websites including repositories
such as github and gitlab.  This copyright statement should not be removed
or edited.

We do grant permission to share solutions privately with non-students such
as potential employers. However, sharing with other current or future
students of CS 7646 is prohibited and subject to being investigated as a
GT honor code violation.

-----do not edit anything above this line---

Student Name: Rahul Jayakrishnan
GT User ID: rjayakrishnan3
GT ID: 903281837 
"""
import marketsimcode as ms
import indicators as ind
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data
from scipy.ndimage.interpolation import shift
import scipy.optimize as spo
import matplotlib.dates as mdates

def bench(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 31), \
          syms=['JPM']):
    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    ben = prices.copy()
    ben.ix[:] = 0
    ben.ix[0, :] = 1000
    return ben

def testPolicy(symbol = "JPM", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000):
    syms=[symbol]
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    optimal = prices.copy()
    long = prices.copy()
    short=prices.copy()
    optimal[:]=0
    long[:] = float('NaN')
    stock=0
    sma,bband,trix=ind.indicators(sd,ed,syms,lookback=14)
    for days in range (prices.shape[0]):
        if sma.ix[days,0] < 0.90 and bband.ix[days,0] < 0 :
            #buy stock
            if stock == 0:
                stock=stock+1000
                optimal.ix[days,0]=1000
                long.ix[days,0]=1
            elif stock== -1000:
                stock=stock+2000
                optimal.ix[days, 0] = 2000
                long.ix[days, 0] = 1
            else:
                optimal.ix[days, 0]=0
        elif sma.ix[days,0] > 1.1 and bband.ix[days,0] > 0 :
            if stock == 0:
                stock=stock-1000
                optimal.ix[days,0]=-1000
                long.ix[days, 0] = -1
            elif stock== 1000:
                stock=stock-2000
                optimal.ix[days, 0] = -2000
                long.ix[days, 0] = -1
            else:
                optimal.ix[days, 0]=0
        elif sma.ix[days,0] >= 1.03 and sma.ix[days-1,0] < 0.9:
            if stock == 0:
                stock=stock-1000
                optimal.ix[days,0]=-1000
                long.ix[days, 0] = -1
            elif stock== 1000:
                stock=stock-2000
                optimal.ix[days, 0] = -2000
                long.ix[days, 0] = -1
            else:
                optimal.ix[days, 0]=0
        elif sma.ix[days,0] <= 1.03 and sma.ix[days-1,0] > 0.9:
            if stock == 0:
                stock=stock+1000
                optimal.ix[days,0]=1000
                long.ix[days, 0] = 1
            elif stock== -1000:
                stock=stock+2000
                optimal.ix[days, 0] = 2000
                long.ix[days, 0] = 1
            else:
                optimal.ix[days, 0]=0
    return optimal,long

def stats(port_val):
    port_val=port_val.values
    cr = (port_val[-1] / port_val[0]) - 1
    dr = port_val / shift(port_val, 1, cval=np.NaN) - 1
    dr = dr[1:]
    adr = dr.mean()
    sddr = dr.std()
    sr = np.sqrt(252) * (dr - 0).mean() / sddr
    print "Cumulative Return:",cr
    print "Average Daily Return:", adr
    print "Standard Deviation of Daily Return:", sddr
    print "Sharp Ratio:", sr
    return cr,sr,adr,sddr

def test_code():
    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009, 12, 31)
    symbols = ['JPM']
    dates = pd.date_range(start_date, end_date)

    prices_all = get_data(symbols, dates)  # automatically adds SPY
    prices = prices_all[symbols]
    ben=bench(sd=start_date, ed=end_date, \
          syms=symbols)
    ret= ms.compute_portvals(ben,symbols,start_val=100000,commission=9.95,impact=0.005)
    benchmark=ret/ret.ix[0,:]
    print "Stats-benchmark"
    stats(ret)
    optimal,long=testPolicy('JPM',start_date,end_date,sv=100000)
    ret1 = ms.compute_portvals(optimal, symbols, start_val=100000, commission=9.95, impact=0.005)
    man=ret1/ret1.ix[0,:]

    print "Stats-Manual Stratagy"
    stats(ret1)
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111)
    plt.xlabel("Date")
    plt.ylabel("Normalised value")
    ax.plot(benchmark, 'b', label="Benchmark",linewidth=0.7)
    ax.plot(man, 'k', label="Manual Stratagy",linewidth=0.7)

    for index, row in prices.iterrows():
        if long.at[index,'JPM']==1:
            plt.axvline(x=index.date(),color="green",linewidth=0.7)
        elif long.at[index,'JPM']==-1:
            plt.axvline(x=index.date(), color="red",linewidth=0.7)

    plt.title("Benchmark vs Manual stratagy [IN SAMPLE]")
    plt.legend(loc="best")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    #plt.xticks(np.arange(start_date,end_date,step=30,dtype='datetime64[D]'),rotation='vertical')
    plt.grid(True)
    plt.savefig("manual.png")
    plt.close()



if __name__ == "__main__":
    test_code()
