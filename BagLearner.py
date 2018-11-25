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
import RTLearner as rtl
import numpy as np
import pdb

class BagLearner(object):

    def __init__(self,learner= rtl.RTLearner, kwargs = {"argument1":1, "argument2":2}, bags = 20, boost = False, verbose = False):
        self.learners=[]
        self.model=[]
        for i in range(0, bags):
            self.learners.append(learner(**kwargs))
        self.bags=bags
        self.verbose=verbose
        pass  # move along, these aren't the drones you're looking for

    def author(self):
        return 'rjayakrishnan3'  # replace tb34 with your Georgia Tech username


    def addEvidence(self, dataX, dataY):
        np.random.seed(98122)
        for i in range(0, self.bags):
            newdataX=np.copy(dataX)
            newdataY=np.copy(dataY)
            for j in range(dataX.shape[0]):
                    rand=np.random.randint(0,len(dataY))
                    tobeapx= dataX[rand,:]
                    tobeapy=dataY[rand]
                    newdataX[j,:]=tobeapx
                    newdataY[j,]=tobeapy
            newdataY=np.reshape(newdataY,(len(newdataY),))
            self.model.append(self.learners[i].addEvidence(newdataX,newdataY))
        return self.model





    def query(self, points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        allpredictions=np.empty(shape=(len(self.model),len(points)))
        for i in range (len(self.model)):
            allpredictions[i,:]=self.learners[i].query(points)

        predictions=np.mean(allpredictions,axis=0)
        return predictions



if __name__ == "__main__":
    print "the secret clue is 'zzyzx'"
