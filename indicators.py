
import pandas as pd  		   	  			    		  		  		    	 		 		   		 		  
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			    		  		  		    	 		 		   		 		  
from util import get_data, plot_data
from scipy.ndimage.interpolation import shift
import scipy.optimize as spo


def indicators(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], lookback=14):
  		   	  			    		  		  		    	 		 		   		 		  
    # Read in adjusted closing prices for given symbols, date range  		   	  			    		  		  		    	 		 		   		 		  
    dates = pd.date_range(sd, ed)  		   	  			    		  		  		    	 		 		   		 		  
    prices_all = get_data(syms, dates)  # automatically adds SPY  		   	  			    		  		  		    	 		 		   		 		  
    price = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    price_high=get_data(syms, dates,colname='High')
    price_high=price_high[syms]
    price_low = get_data(syms, dates, colname='Low')
    price_low = price_low[syms]
    price_close = get_data(syms, dates, colname='Close')
    price_close = price_close[syms]
    volume = get_data(syms, dates, colname='Volume')
    volume = volume[syms]
    #SMA Computation
    sma=price.rolling(window=lookback,min_periods=lookback).mean()
    psma=price/sma
    normprice=price/price.ix[0,:]
    normsma=sma/sma.ix[15,:]
    fig = plt.figure(figsize=(15,10))
    ax=fig.add_subplot(111)
    plt.xlabel("Date",size=15)
    plt.ylabel("Normalised value")
    ax.plot(normprice, label="Price")
    ax.plot(psma, label="Price SMA ratio")
    ax.plot(normsma, label="SMA")
    plt.title("Price to SMA ratio Indicator")
    plt.legend(loc="best")
    plt.xticks(size=15)
    plt.grid(True)
    plt.savefig("PreceSMA.png")
    plt.close()
    #Boli calculation
    rolling_std= price.rolling(window=lookback,min_periods=lookback).std()
    upperband=sma+(2*rolling_std)
    lowerband=sma-(2*rolling_std)
    bbp=(price - lowerband)/(upperband-lowerband)
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111)
    plt.xlabel("Date")
    plt.ylabel("Normalised value")
    plt.plot(normprice, label="Price")
    ax.plot(bbp, label="Bolinger Band")
    ax.plot(upperband/upperband.ix[15,:], label="Upper Band")
    ax.plot(lowerband/lowerband.ix[15,:], label="Lower Band")
    plt.title("Bolinger Band Indicator")
    plt.legend(loc="best")
    plt.xticks(size=15)
    plt.grid(True)
    plt.savefig("Bband.png")
    plt.close()
    #print bbp
    EX1 = price.ewm(span=lookback, min_periods=lookback,axis=0).mean()
    EX2 = EX1.ewm(span=lookback, min_periods=lookback,axis=0).mean()
    EX3 = EX2.ewm(span=lookback, min_periods=lookback,axis=0).mean()

    trix=EX1.copy()
    trix[:]=float('NaN')
    for s in range (len(syms)):
        for i in range (EX3.shape[0]-1):
            trix.ix[i+1,s]=( EX3.ix [i+1,s] - EX3.ix [i,s] ) / EX3.ix [i,s]
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111)
    plt.xlabel("Date")
    plt.ylabel("Normalised value")
    ax.plot(normprice, label="Price")
    ax.plot(trix/trix.ix[40,:]/100, label="trix")
    ax.plot(EX1 / EX1.ix[13, :], label="1st Smoothened EMA")
    ax.plot(EX2 / EX2.ix[26, :], label="2nd Smoothened EMA")
    ax.plot(EX3 / EX3.ix[39, :], label="3rd Smoothened EMA")
    plt.title("Trix Indicator")
    plt.legend(loc="best")
    plt.xticks(size=15)
    plt.grid(True)
    plt.savefig("Trix.png")
    plt.close()
    return psma,bbp,trix



def test_code():

  		   	  			    		  		  		    	 		 		   		 		  
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2009,12,31)
    symbols = ['JPM']
  		   	  			    		  		  		    	 		 		   		 		  
    # Assess the portfolio  		   	  			    		  		  		    	 		 		   		 		  
    indicators(sd = start_date, ed = end_date,\
        syms = symbols)

if __name__ == "__main__":  		   	  			    		  		  		    	 		 		   		 		  
    # This code WILL NOT be called by the auto grader  		   	  			    		  		  		    	 		 		   		 		  
    # Do not assume that it will be called  		   	  			    		  		  		    	 		 		   		 		  
    test_code()  		   	  			    		  		  		    	 		 		   		 		  
