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
  		   	  			    		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			    		  		  		    	 		 		   		 		  
import pandas as pd  		   	  			    		  		  		    	 		 		   		 		  
import util as ut  		   	  			    		  		  		    	 		 		   		 		  
import random
import BagLearner as bl
import RTLearner as rtl
import indicators as ind
import numpy as np
import marketsimcode as ms
from scipy.ndimage.interpolation import shift
  		   	  			    		  		  		    	 		 		   		 		  
class StrategyLearner(object):  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # constructor  		   	  			    		  		  		    	 		 		   		 		  
    def __init__(self, verbose = False, impact=0.0):  		   	  			    		  		  		    	 		 		   		 		  
        self.verbose = verbose  		   	  			    		  		  		    	 		 		   		 		  
        self.impact = impact

  		   	  			    		  		  		    	 		 		   		 		  
    # this method should create a QLearner, and train it for trading  		   	  			    		  		  		    	 		 		   		 		  
    def addEvidence(self, symbol = "JPM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000):  		   	  			    		  		  		    	 		 		   		 		  

        syms=[symbol]  		   	  			    		  		  		    	 		 		   		 		  
        dates = pd.date_range(sd, ed)  		   	  			    		  		  		    	 		 		   		 		  
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY  		   	  			    		  		  		    	 		 		   		 		  
        prices = prices_all[syms]  # only portfolio symbols  		   	  			    		  		  		    	 		 		   		 		  
        if self.verbose: print prices
        self.learner = bl.BagLearner(learner=rtl.RTLearner, kwargs={"leaf_size": 5, "verbose": False}, bags=20, boost=False,
                                verbose=False)
        psma, bbp, trix= ind.indicators(sd,ed,syms,14)
        DataX=np.hstack([np.array(psma),np.array(bbp),np.array(trix)])
        DataY=np.array(prices)
        self.model=self.learner.addEvidence(DataX[40:,:],DataY[40:,:])
        return self.model


  		   	  			    		  		  		    	 		 		   		 		  
        # # example use with new colname
        # volume_all = ut.get_data(syms, dates, colname = "Volume")  # automatically adds SPY
        # volume = volume_all[syms]  # only portfolio symbols
        # volume_SPY = volume_all['SPY']  # only SPY, for comparison later
        # if self.verbose: print volume
  		   	  			    		  		  		    	 		 		   		 		  
    # this method should use the existing policy and test it against new data  		   	  			    		  		  		    	 		 		   		 		  
    def testPolicy(self, symbol = "JPM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
        # here we build a fake set of trades  		   	  			    		  		  		    	 		 		   		 		  
        # your code should return the same sort of data
        syms=[symbol]
        dates = pd.date_range(sd, ed)  		   	  			    		  		  		    	 		 		   		 		  
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        price=prices_all[syms]
        trades = prices_all[[symbol,]]  # only portfolio symbols
        trades.values[:,:] = 0 # set them all to nothing
        psma, bbp, trix = ind.indicators(sd, ed, syms, 14)
        DataX = np.hstack([np.array(psma), np.array(bbp), np.array(trix)])
        predict=self.learner.query(DataX[40:,:])
        holdings=0
        for days in range (trades.shape[0]-1):
            temp=trix.ix[days]
            temp=pd.to_numeric(temp,downcast='float')[0]
            if pd.isnull(temp):
                continue
            else:

                prediction=predict[days-40+1]
                current_price=pd.to_numeric(price.ix[days],downcast='float')[0]
                if holdings>0:
                    if current_price>prediction:
                        trades.ix[days]=-2000

                elif holdings<0:
                    if current_price<prediction:
                        trades.ix[days] = 2000
                else:
                    if current_price > prediction:
                        trades.ix[days] = -1000
                    elif current_price<prediction:
                        trades.ix[days] = 1000
                holdings=holdings+pd.to_numeric(trades.ix[days],downcast='float')[0]
        return trades

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
if __name__=="__main__":
    learner= StrategyLearner(verbose=False,impact=0)
    learner.addEvidence(symbol='JPM',sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,12,31), \
        sv = 100000)
    trades=learner.testPolicy(symbol='JPM',sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,12,31), \
        sv = 100000)
    port=ms.compute_portvals(trades,['JPM'],commission=0,impact=0,start_val=100000)
    stats(port)
    print "One does not simply think up a strategy"

