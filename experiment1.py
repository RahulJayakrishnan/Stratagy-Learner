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
import StrategyLearner as stl
import ManualStratagy as manual


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

def test_code():
    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009, 12, 31)
    symbols = ['JPM']
    dates = pd.date_range(start_date, end_date)

    prices_all = get_data(symbols, dates)  # automatically adds SPY
    prices = prices_all[symbols]
    long=prices.copy()
    ben=bench(sd=start_date, ed=end_date, \
          syms=symbols)
    ret= ms.compute_portvals(ben,symbols,start_val=100000,commission=0,impact=0)
    benchmark=ret/ret.ix[0,:]
    print "Stats-benchmark"
    stats(ret)
    learner = stl.StrategyLearner(verbose=False, impact=0.0)
    learner.addEvidence(symbol=symbols[0], sd=start_date, \
                        ed=end_date, \
                        sv=100000)
    trades = learner.testPolicy(symbol=symbols[0], sd=start_date, \
                        ed=end_date, \
                        sv=100000)
    port = ms.compute_portvals(trades, ['JPM'], commission=0, impact=0.00, start_val=100000)
    print "Stats-Learner Stratagy"
    stats(port)
    port=port/port[0]
    long[:]=0
    count=0
    for day in range (trades.shape[0]):
        temp=trades.ix[day][0]
        if temp>0:
            count+=1
            long.ix[day][0]=1
        elif temp<0:
            count += 1
            long.ix[day][0]=-1
    print "total trades:",count
    optimal, long = manual.testPolicy('JPM', start_date, end_date, sv=100000)
    ret1 = ms.compute_portvals(optimal, symbols, start_val=100000, commission=0, impact=0)
    man = ret1 / ret1.ix[0, :]

    print "Stats-Manual Stratagy"
    stats(ret1)

    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111)
    plt.xlabel("Date")
    plt.ylabel("Normalised Portfolio value")
    ax.plot(benchmark, 'b', label="Benchmark",linewidth=0.7)
    ax.plot(port, 'k', label="Stratagy Learner",linewidth=0.7)
    ax.plot(man, 'r', label="Manual Stratagy", linewidth=0.7)

    # for index, row in prices.iterrows():
    #     if long.at[index,'JPM']==1:
    #         plt.axvline(x=index.date(),color="green",linewidth=0.7)
    #     elif long.at[index,'JPM']==-1:
    #         plt.axvline(x=index.date(), color="red",linewidth=0.7)

    plt.title("Manual Stratagy vs Stratagy Learner [IN SAMPLE]")
    plt.legend(loc="best")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    #plt.xticks(np.arange(start_date,end_date,step=30,dtype='datetime64[D]'),rotation='vertical')
    plt.grid(True)
    plt.savefig("ManVsLearner.png")
    plt.close()

if __name__=="__main__":
    test_code()
