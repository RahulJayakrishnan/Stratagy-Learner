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

Student Name: Rahul Jayakrishnan (replace with your name)
GT User ID: rjayakrishnan3 (replace with your User ID)
GT ID: 903281837 (replace with your GTID)
"""  		
import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data


def author():
    return 'rjayakrishnan3'  # replace tb34 with your Georgia Tech username.

def compute_portvals(trades,syms, start_val = 1000000, commission=9.95, impact=0.005):
    orders_df = trades
    start_date = orders_df.index[0]
    end_date = orders_df.index[-1]
    sym=syms
    date = pd.date_range(start_date, end_date, freq='D')
    prices_all = get_data(sym, pd.date_range(start_date, end_date))
    df_prices = prices_all[sym]
    df_prices.drop(df_prices.columns[0], axis=1)
    df_prices['Cash'] = 1.0
    df_trades = pd.DataFrame(columns=syms, index=df_prices.index)
    df_trades['Cash'] = 'NaN'
    df_trades[:] = 0
    for index, row in orders_df.iterrows():
        for i in range (len(sym)):
            if trades.at[index,sym[i]] > 0:
                df_trades.at[index, sym[i]] = trades.at[index, sym[i]]
                df_trades.at[index, 'Cash'] = df_trades.at[index, 'Cash'] - (
                        trades.at[index, sym[i]] * df_prices.at[index, sym[i]]) * (1 + impact) - commission

            elif trades.at[index,sym[i]] < 0:
                df_trades.at[index, sym[i]] = trades.at[index, sym[i]]
                df_trades.at[index, 'Cash'] = df_trades.at[index, 'Cash'] + -trades.at[index, sym[i]] * df_prices.at[
                    index, sym[i]] * (1 - impact) - commission

    df_holdings = pd.DataFrame(columns=syms, index=df_prices.index)
    df_holdings['Cash'] = 'NaN'
    df_holdings[:] = 0
    for index, row in df_trades.iterrows():

        if index == df_trades.index[0]:
            for i in sym:
                prev_index = index
                df_holdings.at[index, i] = df_trades.at[index, i]
            df_holdings.at[index, 'Cash'] = start_val + df_trades.at[index, 'Cash']
        else:
            for i in sym:
                df_holdings.at[index, i] = df_holdings.at[prev_index, i]
            df_holdings.at[index, 'Cash'] = df_holdings.at[prev_index, 'Cash']
            prev_index = index
            for i in sym:
                df_holdings.at[index, i] = df_holdings.at[index, i] + df_trades.at[index, i]
            df_holdings.at[index, 'Cash'] = df_holdings.at[index, 'Cash'] + df_trades.at[index, 'Cash']

    # print df_holdings

    df_values = df_holdings
    for index, row in df_values.iterrows():
        if index in df_prices.index:
            for i in sym:
                df_values.at[index, i] = df_values.at[index, i] * df_prices.at[index, i]
                prev_index = index
        else:
            for i in sym:
                df_values.at[index, i] = df_values.at[prev_index, i]
                prev_index = index

    portvals = df_values.sum(axis=1)

    return portvals


def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    syms = ['JPM']
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    ben = prices.copy()
    ben.ix[:] = 0
    ben.ix[0, :] = 1000

if __name__ == "__main__":
    test_code()