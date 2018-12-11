#
# 
import numpy as np
import matplotlib as mplib
import urllib2
import json
import re
import sys
from time import sleep



host = sys.argv[1]
try:
    iterations = int(sys.argv[2])
except:
    iterations = 100
port = str(5005) #sys.argv[2]
url = 'http://'+host+':'+port
print url



class bombyCar:
    def __init__(self,initState,state_tt,sensor_tt):
        self.bel = initState
        self.state_tt = state_tt
        self.sensor_tt = sensor_tt
        print "initial belief: "
        print self.bel
        print "state transition: "
        print self.state_tt
        print "sensor transition: "
        print self.sensor_tt

    def getBel(self):
        return self.bel

    def getSensor(self):
        return self.sensor_tt

    def getState(self):
        return self.state_tt

    def getIndexOfRange(self, obs):
        if obs < 20:
            index = 0
        elif obs >= 20 and obs < 30:
            index = 1
        elif obs >= 30 and obs < 40:
            index = 2
        elif obs >= 40 and obs < 50:
            index = 3
        elif obs >= 50 and obs < 60:
            index = 4
        elif obs >= 60:
            index = 5
        return index

    def bayesBelief(self, obs, act):
        bel_ = self.bel*self.state_tt[act]
        bel = np.multiply(bel_,self.sensor_tt[:,obs].T)
        self.bel = bel*1/np.sum(bel)

def getObsSim():
    obs = int(input("observed distance is [cm]: "))
    return obs

def chooseActSim():
    action = len(raw_input("Action is\n\tpress enter to move\n\tpress 1 to stop: "))
    action = 1 if action > 0 else 0
    return action

def getObs():
    try:
        contents = urllib2.urlopen(url+'/',timeout=6)
        data = contents.read()
        js = json.loads(data)
        dataIs = {'dist':js['dist'],'number':js['numero']}
        # print dataIs
    except:
        dataIs = {'dist':-1,'number':0}
        # print dataIs
    return dataIs

def executeChooseAct(moreProbState):
    action = 'S' if moreProbState == 0 else 'B'
    print "The action is: ", "move" if action == 'B' else "stop"
    try:
        contents = urllib2.urlopen(url+'/'+action,timeout=6)
        data = contents.read()
        success = 0
    except:
        success = 1
    return success



def simulate(bel_t,state_tt,sensor_tt):
    bomby = bombyCar(bel_t,state_tt,sensor_tt)
    go = True
    count = 0
    act = 1
    while(go and count < iterations):
        count += 1
        obs = getObs()
        print obs['dist']
        if obs['dist'] < 0:
            continue
        # print "valid number so, start the calculations"
        index = bomby.getIndexOfRange(obs['dist'])
        # print index
        bomby.bayesBelief(index, act)
        creer = bomby.getBel()
        print "\tRequest: ",obs['number'],"\tObject is in distance range #: ",creer.argmax()+1 
        print "\tBomby's belief dist: ",creer
        ind_maximo = creer.argmax()
        print "\tprobability on range",creer.item(ind_maximo)
        # act = input("insert action [0 move, 1 stop]: ")
        act = executeChooseAct(bomby.getBel().argmax()) # this will be chosen depending on the belief distribution
        print "\tSucess to move" if act == 0 else "Failure to move"
        
        sleep(0.5) # wait 500 ms
        # print "at some point make the car not move more and stop simulation"
        # make go = False



if __name__ == "__main__":
    belief = np.matrix([1.0/6,1.0/6,1.0/6,1.0/6,1.0/6,1.0/6]) # robot doesnot know anything
# state_tt = np.matrix([[0.8,0.15,0.05],[0.4,0.4,0.2],[0.2,0.6,0.2]]) # today\trw
# state_tt[0] = transition tables for action GO
# state_tt[1] = transition tables for action Do nothing
    state_tt = [np.matrix([[0.50,0.10,0.10,0.10,0.10,0.10]
                          ,[0.70,0.10,0.05,0.05,0.05,0.05]
                          ,[0.05,0.70,0.10,0.05,0.05,0.05]
                          ,[0.05,0.05,0.70,0.10,0.05,0.05]
                          ,[0.05,0.05,0.05,0.70,0.10,0.05]
                          ,[0.05,0.05,0.05,0.05,0.10,0.87]]),
                np.matrix([[1.00,0.00,0.00,0.00,0.00,0.00]
                          ,[0.00,1.00,0.00,0.00,0.00,0.00]
                          ,[0.00,0.00,1.00,0.00,0.00,0.00]
                          ,[0.00,0.00,0.00,1.00,0.00,0.00]
                          ,[0.00,0.00,0.00,0.00,1.00,0.00]
                          ,[0.00,0.00,0.00,0.00,0.00,1.00]])]


    # reality \ sensor says
    sensor_tt = np.matrix([[0.91,0.05,0.01,0.01,0.01,0.01]
                          ,[0.05,0.87,0.05,0.01,0.01,0.01]
                          ,[0.01,0.05,0.87,0.05,0.01,0.01]
                          ,[0.01,0.01,0.05,0.87,0.05,0.01]
                          ,[0.01,0.01,0.01,0.05,0.87,0.05]
                          ,[0.01,0.01,0.01,0.01,0.01,0.95]]) 
    simulate(belief,state_tt,sensor_tt)

