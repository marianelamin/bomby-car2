'''
    Simple Kalman Filter given initial matrices.
'''
import numpy as np
import math
import random
import pylab

def kalman(mu,sigma,u,z,A,B,R,Q,C):
    '''
        mu = mean at t-1
        sigma = cov at t-1
        u = controls at t
        z = sensors at t
        A = state transition equations at t
        B = controls contributions to state transition at t
        R = covariance of the error of state transition at t
        Q = covariance of the error of sensor corrections at t
        C = equations to go from sensor data to a state
    '''
    mu_ = A*mu+B*u
    sigma_ = A*sigma*A.T+R
    K = sigma_*C.T*(C*sigma_*C.T+Q).I
    mu = mu_+K*(z-C*mu_)
    sigma = (np.eye(np.size(mu))-K*C)*sigma_
    return(mu,sigma)

# Auxiliary functions to simulate
def simulate(mu,sigma,A,B,C,R,Q,dt,noise,z_noise,motion):
    c = CarWithSensor(mu,A,B,C,R,Q,dt,noise,z_noise,motion)
    u = c.getU()
    z = float(c.getZ()[0]) # noisy X
    x = [c.getX()]
    v = [c.getV()]
    kx = [float(mu[0][0])]
    kv = [float(mu[1][0])]
    nx = [z]
    nv = [c.getV()]
    zx = [z]
    C_i = C.I
    it = [0]
    for i in range(iterations):
        mu,sigma = kalman(mu,sigma,u,z,A,B,R,Q,C)
        c.step()
        z = c.getZ()
        u = c.getU()
        x.append(c.getX())
        v.append(c.getV())
        kx.append(float(mu[0][0]))
        kv.append(float(mu[1][0]))
        nx.append(float((C_i*z)[0]))
        nv.append(c.getV())
        it.append(i+1)
        #print z
    #print len(it), len(x), len(nx), len(kx)
    #print mu
    #print sigma
    #print nx
    #print x
    #print kx
    pylab.plot(it,x,'-')
    pylab.plot(it,nx,'-')
    pylab.plot(it,kx,'--')
    pylab.xlabel('Iterations')
    pylab.ylabel('Distance')
    pylab.title('Measurement of a Moving Car')
    pylab.legend(('Physics','Beacon','Kalman'))
    pylab.show()

# The idea here is a moving object  with a sensor
# and at each time step the sensor senses data and the
# moving robot also estimates where it is at.

# The parameters of this object are the A, B, C, Q and R matrices, together with
# the initial state, the process estimation noise and the sensor noise.
# lastly, there is a parameter for the action of the controllers.
class CarWithSensor:
    def __init__(self,Xo,A,B,C,R,Q,ts,pos_noise,z_noise,action):
        self.dt = ts # 1 second
        self.X = Xo
        self.v = Xo[0][0] # 10 miles per hour
        self.x = float(Xo[1][0]) # starts from the beacon
        self.light =  299792458.0
        self.pos_noise = pos_noise
        self.z_noise = z_noise
        self.action = action
        self.A = A
        self.B = B
        self.C = C
        self.R = R
        self.Q = Q

    # at each timestep, move the car (in theory, where it should be)
    def step(self):
        e = (np.full(self.X.shape,random.gauss(0,self.pos_noise)))
        self.X = self.A*self.X+self.B*self.getU()
        self.x = float(self.X[0][0])
        self.X = self.X+e

    def getU(self):
        if self.action=='stop':
            return -2 #f/m
        elif self.action=='forward':
            return 1.5
        else:
            return 0


    def getX(self):
        return self.x

    def getV(self):
        return self.X[1][0]

    def getZ(self):
        #print "X",self.X,self.C
        z_ = self.C*self.X
        d = Q*np.full(z_.shape,random.gauss(0,z_noise))
        #print d
        z = z_+d
        if z[0]<0.0:
            z[0]=0.0
        return z


if __name__=="__main__":
    # This program assumes one sensor and a
    # state comprised of distance (X) and speed (V).
    # |X|
    # |V|
    #
    # Default
    dt = 0.1
    iterations = 300
    A=np.matrix([[1,dt],
                 [0,1]])
    B=np.matrix([[dt**2/2.0],
                 [dt]])
    noise=0.5 # The noise in the process (movement)
    z_noise = 2 # noise in the sensor (measurements)
    R = np.matrix([[1,0],
                   [0,1]]) # process covariance
    Q = np.matrix([z_noise]) # measurement (sensor) covariance.
    C = np.matrix([1.0,0.0]) # Converts state to sensor data.
    mu = np.matrix([[0],
                    [0]]) # estimated position of the model.
    sigma = np.matrix([[1,0],
                       [0,1]]) # The covariance of the model.
    motion = "forward" # can be forward, stop or none.

    # Do not touch what follows.
    # It just iterates over the Kalman filter and plots that.
    simulate(mu,sigma,A,B,C,R,Q,dt,noise,z_noise,motion)