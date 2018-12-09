import numpy as np
import matplotlib as mplib

class bombyCar:
    def __init__(self,alpha,state_tt,sensor_tt):
        self.alpha = alpha
        self.state_tt = state_tt
        self.sensor_tt = sensor_tt
        print "state transition: "
        print self.state_tt
        print "sensor transition: "
        print self.sensor_tt

    def getAlpha(self):
        return self.alpha

    def getSensor(self):
        return self.sensor_tt

    def getState(self):
        return self.state_tt

    def nextDist_bayes(self, obs):
        alpha_new = np.multiply(self.alpha*self.state_tt,self.sensor_tt[:,obs-1].T)
        self.alpha = alpha_new*1/np.sum(alpha_new)

def getObs():
    print "Elige tu observacion:"
    print "\t1. sunny"
    print "\t2. cloudy"
    print "\t3. rainy"
    obs = int(input())
    return obs


def simulate(alpha,state_tt,sensor_tt):
    bomby = bombyCar(alpha,state_tt,sensor_tt)
    while(True):
        obs = getObs()
        print "current alpha"
        bomby.nextDist_bayes(obs)
        print bomby.getAlpha().T
        # print alpha.T


if __name__ == "__main__":
    alpha = np.matrix([1, 0, 0])
    state_tt = np.matrix([[0.8,0.15,0.05],[0.4,0.4,0.2],[0.2,0.6,0.2]]) # today\trw
    sensor_tt = np.matrix([[0.6,0.4,0],[0.3,0.7,0],[0,0,1]]) # actual\says
    simulate(alpha,state_tt,sensor_tt)

