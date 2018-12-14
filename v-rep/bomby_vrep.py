#
# 
import numpy as np
import matplotlib as mplib
import matplotlib.pyplot as plt
import urllib2
import time, sys, re, json
from time import sleep
import vrep



class bombyCar:
    def __init__(self,initState,state_tt,sensor_tt,action,ranges):
        self.bel = initState
        self.state_tt = state_tt
        self.sensor_tt = sensor_tt
        self.action = action
        print "initial belief: "
        print self.bel
        print "state transition: "
        print self.state_tt
        print "sensor transition: "
        print self.sensor_tt
        self.rangeDist = ranges

    def getBel(self):
        return self.bel

    def getSensor(self):
        return self.sensor_tt

    def getAct(self):
        return self.action

    def getState(self):
        return self.state_tt

    def setAct(self, val):
        self.action = val

    def getIndexOfRange(self, obs):
        if obs < self.rangeDist[0]:
            index = 0
        elif obs >= self.rangeDist[0] and obs < self.rangeDist[1]:
            index = 1
        elif obs >= self.rangeDist[1] and obs < self.rangeDist[2]:
            index = 2
        elif obs >= self.rangeDist[2] and obs < self.rangeDist[3]:
            index = 3
        elif obs >= self.rangeDist[3] and obs < self.rangeDist[4]:
            index = 4
        elif obs >= self.rangeDist[4]:
            index = 5
        return index

    # def execAct(self):
    #     moreProbState = self.bel.argmax()
    #     action = 'S' if moreProbState == 0 else 'B'
    #     print "The action is: ", "move" if action == 'B' else "stop"
    #     try:
    #         contents = urllib2.urlopen(url+'/'+action,timeout=6)
    #         data = contents.read()
    #         self.action = 0
    #     except:
    #         self.action = 1
    #         return self.action

    def execAct(self,bRob):
        moreProbState = self.bel.argmax()
        action = 'S' if moreProbState == 0 else 'B'


        print "The action is: ", "move" if action == 'B' else "stop"
        try:
            contents = urllib2.urlopen(url+'/'+action,timeout=6)
            data = contents.read()
            self.action = 0
        except:
            self.action = 1
            return self.action

    def bayesBelief(self, obs):
        bel_ = self.bel*self.state_tt[self.action]
        bel = np.multiply(bel_,self.sensor_tt[:,obs].T)
        self.bel = bel*1/np.sum(bel)

# def getObsSim():
#     obs = int(input("observed distance is [cm]: "))
#     return obs

# def chooseActSim():
#     action = len(raw_input("Action is\n\tpress enter to move\n\tpress 1 to stop: "))
#     action = 1 if action > 0 else 0
#     return action

# def getObs():
#     try:
#         contents = urllib2.urlopen(url+'/',timeout=6)
#         data = contents.read()
#         js = json.loads(data)
#         dataIs = {'dist':js['dist'],'number':js['numero']}
#         # print dataIs
#     except:
#         dataIs = {'dist':-1,'number':0}
#         # print dataIs
#     return dataIs

# def executeChooseAct(moreProbState):
#     action = 'S' if moreProbState == 0 else 'B'
#     print "The action is: ", "move" if action == 'B' else "stop"
#     try:
#         contents = urllib2.urlopen(url+'/'+action,timeout=6)
#         data = contents.read()
#         success = 0
#     except:
#         success = 1
#     return success

def get_bel_arr(bel):
    return bel.item(0),bel.item(1),bel.item(2),bel.item(3),bel.item(4),bel.item(5)


def prettyHistShow(plotSub,plotBar,inf,pdf):
    z1,z2,z3,z4,z5,z6 = get_bel_arr(pdf)
    action = 'Move' if inf[2] == 0 else 'Stop'
    plt.title('Probability Distribution of Robots Belief\nRequest: '+str(inf[0])+' - Distance:'+str(round(inf[1],2))+' - Action:'+action)
    plotSub[1].set_xticklabels(['Zone1\n('+str(round(z1,2))+')', 'Zone2 \n('+str(round(z2,2))+')', 'Zone3 \n('+str(round(z3,2))+')','Zone4 \n('+str(round(z4,2))+')','Zone5 \n('+str(round(z5,2))+')','Zone6 \n('+str(round(z6,2))+')'])
    # update the animated artists
    plotBar[0].set_height(z1)
    plotBar[1].set_height(z2)
    plotBar[2].set_height(z3)
    plotBar[3].set_height(z4)
    plotBar[4].set_height(z5)
    plotBar[5].set_height(z6)

def simulate(bel_t,state_tt,sensor_tt,brob):
    ranges = [20,30,40,50,60]    #measured in cm
    go = True
    count = 0
    act = 1
    bomby = bombyCar(bel_t,state_tt,sensor_tt,act,ranges)

    # setting up the plot
    plotSub = plt.subplots()
    ind = np.arange(1, 7)
    # show the figure, but do not block
    plt.show(block=False)
    plotBar = plt.bar(ind, get_bel_arr(bomby.getBel()))
    plotSub[1].set_xticks(ind)
    plotSub[1].set_xticklabels(['Zone1', 'Zone2', 'Zone3','Zone4','Zone5','Zone6'])
    plotSub[1].set_ylim([0, 1])
    plotSub[1].set_ylabel('Probability')
    plotSub[1].set_title('Belief')


    #starts the somulation
    t=time.time()
    while (go and count < ITERATIONS) and time.time()-t < TSECONDS :
        count += 1
        #obs = getObs()
        obs = brob.getProxSensor()
        # print obs['dist']
        if obs['dist'] < 0:
            continue
        print "Distance measured by sensor: ",obs['dist']
        # print "valid number so, start the calculations"
        index = bomby.getIndexOfRange(obs['dist'])
        bomby.bayesBelief(index)
        creer = bomby.getBel()
        ind_maximo = creer.argmax()
        print "\tRequest: ",count,"\tBomby's belief dist:"
        print creer
        print "\tObject in distance range #: ",ind_maximo+1 ,"\tProbability:",creer.item(ind_maximo)
        
        # act = input("insert action [0 move, 1 stop]: ")
        # act = execAct() # this will be chosen depending on the belief distribution
        act = brob.exActVrep(bomby)
        print "\tSucess to move" if act == 0 else "Failure to move"
        

        info = [count, obs['dist'], act]
        prettyHistShow(plotSub,plotBar,info,bomby.getBel())

        plotSub[0].canvas.draw_idle()
        try:
            plotSub[0].canvas.flush_events()
        except NotImplementedError:
            pass



        sleep(0.5) # wait 500 ms
        # print "at some point make the car not move more and stop simulation"
        # make go = False
    print " ALL DONE!"



class bubbleVrep:
    def __init__(self,clientID):
        self.clientID = clientID
        error_code, self.l_motor_handle = vrep.simxGetObjectHandle(self.clientID,"bubbleRob_leftMotor",vrep.simx_opmode_blocking)
        error_code, self.r_motor_handle = vrep.simxGetObjectHandle(self.clientID,"bubbleRob_rightMotor",vrep.simx_opmode_blocking)
        error_code, self.ps_handle = vrep.simxGetObjectHandle(self.clientID,"bubbleRob_sensingNose",vrep.simx_opmode_blocking)
        error_code, self.camera = camera = vrep.simxGetObjectHandle(self.clientID, 'Vision_sensor', vrep.simx_opmode_blocking)


    def getProxSensor(self):
        err_code, detectionState, detectedPoint,detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(self.clientID, self.ps_handle, vrep.simx_opmode_streaming)
        if err_code == 0 or err_code ==1:
            dataIs = {'dist': np.linalg.norm(detectedPoint)*100}
        else:
            dataIs = {'dist': -1}

        dataIs['number'] = 200
        return dataIs

    def getCamera(self):
        err_code, resolution, image = vrep.simxGetVisionSensorImage(self.clientID, self.camera, 0, vrep.simx_opmode_streaming)
        return [resolution, image] if err_code == 0 else [-1,-1]

    def exActVrep(self,bomby):
        if bomby.getBel().argmax() != 0:
            bomby.setAct(0)
            err_code = vrep.simxSetJointTargetVelocity(self.clientID, self.l_motor_handle, 1.0, vrep.simx_opmode_streaming)
            err_code = vrep.simxSetJointTargetVelocity(self.clientID, self.r_motor_handle, 1.0, vrep.simx_opmode_streaming)
        else:
            bomby.setAct(1)
            err_code = vrep.simxSetJointTargetVelocity(self.clientID, self.l_motor_handle, 0.0, vrep.simx_opmode_streaming)
            err_code = vrep.simxSetJointTargetVelocity(self.clientID, self.r_motor_handle, 0.0, vrep.simx_opmode_streaming)
        print "The action is: ", "move" if bomby.getAct() == 0 else "stop"
        return bomby.getAct()



TSECONDS = int(sys.argv[1])
host = sys.argv[2]
try:
    port = int(sys.argv[3])
except:
    port = 5005
ITERATIONS = 100

# url = 'http://'+host+':'+port
# print url

vrep.simxFinish(-1)



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
                np.matrix([[0.95,0.01,0.01,0.01,0.01,0.01]
                          ,[0.01,0.95,0.01,0.01,0.01,0.01]
                          ,[0.01,0.01,0.95,0.01,0.01,0.01]
                          ,[0.01,0.01,0.01,0.95,0.01,0.01]
                          ,[0.01,0.01,0.01,0.01,0.95,0.01]
                          ,[0.01,0.01,0.01,0.01,0.01,0.95]])]


    # reality \ sensor says
    sensor_tt = np.matrix([[0.91,0.05,0.01,0.01,0.01,0.01]
                          ,[0.05,0.87,0.05,0.01,0.01,0.01]
                          ,[0.01,0.05,0.87,0.05,0.01,0.01]
                          ,[0.01,0.01,0.05,0.87,0.05,0.01]
                          ,[0.01,0.01,0.01,0.05,0.87,0.05]
                          ,[0.01,0.01,0.01,0.01,0.01,0.95]]) 
    

    clientID = vrep.simxStart(host,port,True,True,5000,5)
    print "clientID"
    if clientID != -1:
        print("Connected to remote API Server")
        bRob = bubbleVrep(clientID)
        simulate(belief,state_tt,sensor_tt,bRob)
        vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot)
    else:
        print("Not connected to remote API Server")
        sys.exit("Could not connect")

    
