import LinRegLearner as lrl
import DTLearner as dtl
import RTLearner as rtl
import numpy as np
import pdb

class BagLearner(object):

    def __init__(self,learner= lrl.LinRegLearner, kwargs = {"argument1":1, "argument2":2}, bags = 20, boost = False, verbose = False):
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
