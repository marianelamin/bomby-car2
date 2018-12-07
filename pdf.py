import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

def pdf(x,mu,cov,n):
    c = 1/(np.sqrt(np.power(2*np.pi,n))*np.linalg.det(cov))
    meat = (x-mu).T*cov.I*(x-mu)
    return c*np.exp(-0.5*meat)

def genPDFS(D1,D2):
    ''' takes grid data D1 and D2 and computes Z '''
    d3 =[]
    for d1,d2 in zip(D1,D2):
            d3.append([np.asscalar(pdf(np.matrix([[i],[j]]),mu,cov,2)) for i,j in zip(d1,d2)])
    return d3

mu = np.matrix([[4],[2]])
cov = np.matrix([[0.025, 0.015],[0.015,0.09]])
fig = plt.figure()
ax = plt.axes(projection='3d')
x = np.linspace(3.25,4.75,100)
y = np.linspace(1, 3, 100)
X, Y = np.meshgrid(x, y)
Z =genPDFS(X,Y)
ax.contour3D(X, Y, Z, 100)
plt.show()