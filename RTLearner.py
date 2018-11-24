import numpy as np
import pdb

def build_tree(dataX, dataY,leafSize):
    if dataX.shape[0] <= leafSize:
        return np.array([[-1, float(np.mean(dataY)), -1, -1]])
    elif np.unique(dataY).size == 1:
        return np.array([[-1, float(dataY[0]), -1, -1]])

    else:
        i = np.random.randint(0, dataX.shape[1])
        Splitval=np.median(dataX[:,i])
        if np.median(dataX[:,i]) == np.max(dataX[:,i]):
            return np.array([[-1, float(Splitval), -1, -1]])
        x=dataX[np.where(dataX[:,i]<=Splitval)]
        y=dataY[np.where(dataX[:,i]<=Splitval)]
        lefttree = build_tree(x,y,leafSize)
        x = dataX[np.where(dataX[:, i] > Splitval)]
        y = dataY[np.where(dataX[:, i] > Splitval)]
        righttree = build_tree(x,y,leafSize)
        root = np.array([i, Splitval, 1,len(lefttree) + 1])
        return np.vstack((root,lefttree,righttree))






class RTLearner(object):

    def __init__(self,leaf_size=1, verbose=False ):
        self.leafSize=leaf_size;
        self.verb=verbose;
        pass  # move along, these aren't the drones you're looking for

    def author(self):
        return 'rjayakrishnan3'  # replace tb34 with your Georgia Tech username


    def addEvidence(self, dataX, dataY):
        np.seterr(divide='ignore', invalid='ignore')
        self.model_coefs=build_tree(dataX,dataY,self.leafSize)
        return self.model_coefs

    def query(self, points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        prediction =np.zeros(len(points))
        for i in range(len(points)):
            j=0
            while j < len(self.model_coefs):
                    j=int(j)
                    if self.model_coefs[j][0] == -1:
                        prediction[i]=self.model_coefs[j][1]
                        break
                    elif points[i][int(self.model_coefs[j][0])]<=self.model_coefs[j][1]:
                         j=j+self.model_coefs[j][2]
                    else:
                         j = j + self.model_coefs[j][3]
        return prediction


if __name__ == "__main__":
    print "the secret clue is 'zzyzx'"
