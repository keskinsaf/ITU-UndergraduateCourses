"""
    Safa Keskin
    150140137
    BLG454E-LFD
"""

import numpy as np
import matplotlib.pyplot as plt

x1 = []
x2 = []
cs = []

meanc0x1 = [0, 0,0]; meanc1x1 = [0, 0,0]
meanc2x1 = [0, 0,0]; meanc0x2 = [0, 0,0]
meanc1x2 = [0, 0,0]; meanc2x2 = [0, 0,0]

c1x1 = [] ; c1x2 = [];
c2x1 = [] ; c2x2 = [];
c0x1 = [] ; c0x2 = [];

def whichClass(e, i, c):
    global c1x1; global c1x2;
    global c2x1; global c2x2;
    global c0x1; global c0x2;
    if c == 0:
        if i == 1:
            c0x1 += [e]
        else:
            c0x2 += [e]
    elif c == 1:
        if i == 1:
            c1x1 += [e]
        else:
            c1x2 += [e]
    else:
        if i == 1:
            c2x1 += [e]
        else:
            c2x2 += [e]

def findCovariance(c):
    global c1x1; global c1x2; global meanc0x1; global meanc0x2;
    global c2x1; global c2x2; global meanc1x1; global meanc1x2;
    global c0x1; global c0x2; global meanc2x1; global meanc2x2;
    val11 = 0; val12 = 0; val22 = 0;
    if c == 0:
        for i in range(len(c0x1)):
            val11 += (c0x1[i] - meanc0x1[2])**2
            val12 += (c0x1[i] - meanc0x1[2])*(c0x2[i] - meanc0x2[2])
            val22 += (c0x2[i] - meanc0x2[2])**2
        val11 /= (len(c0x1) - 1); val12 /= (len(c0x1) - 1); val22 /= (len(c0x2) - 1);
    if c == 1:
        for i in range(len(c1x1)):
            val11 += (c1x1[i] - meanc1x1[2])**2
            val12 += (c1x1[i] - meanc1x1[2])*(c1x2[i] - meanc1x2[2])
            val22 += (c1x2[i] - meanc1x2[2])**2
        val11 /= (len(c1x1) - 1); val12 /= (len(c1x1) - 1); val22 /= (len(c1x2) - 1);
    if c == 2:
        for i in range(len(c2x1)):
            val11 += (c2x1[i] - meanc2x1[2])**2
            val12 += (c2x1[i] - meanc2x1[2])*(c2x2[i] - meanc2x2[2])
            val22 += (c2x2[i] - meanc2x2[2])**2
        val11 /= (len(c2x1) - 1); val12 /= (len(c2x1) - 1); val22 /= (len(c2x2) - 1);

    return [[val11, val12,],[val12, val22]]

def g( x ): #x = x1 x2 y
    cov0 = findCovariance(0)
    cov1 = findCovariance(1)
    cov2 = findCovariance(2)
    sum = len(c0x1) + len(c1x1) + len(c2x1)

    g0 = -0.5 * np.dot( np.dot(np.transpose( [ x[0] - meanc0x1[2], x[1] - meanc0x2[2] ] ),\
    np.linalg.inv(cov0) ), np.array([ x[0] - meanc0x1[2], x[1] - meanc0x2[2] ])) \
    - 0.5 * np.log( np.linalg.det(cov0) ) + np.log( len(c0x1) / sum )
    g1 = -0.5 * np.dot( np.dot(np.transpose( [ x[0] - meanc1x1[2], x[1] - meanc1x2[2] ] ),\
    np.linalg.inv(cov1) ), np.array([ x[0] - meanc1x1[2], x[1] - meanc1x2[2] ])) \
    - 0.5 * np.log( np.linalg.det(cov1) ) + np.log( len(c1x1) / sum )
    g2 = -0.5 * np.dot( np.dot(np.transpose( [ x[0] - meanc2x1[2], x[1] - meanc2x2[2] ] ),\
    np.linalg.inv(cov2) ), np.array([ x[0] - meanc2x1[2], x[1] - meanc2x2[2] ])) \
    - 0.5 * np.log( np.linalg.det(cov2) ) + np.log( len(c2x1) / sum )

    if max(g0, g1, g2) == g0:
        return 0
    elif max(g0, g1, g2) == g1:
        return 1
    else:
        return 2

#below function is inspired from
#   http://scikit-learn.org/stable/auto_examples/linear_model/plot_iris_logistic.html
def myGraph():
    global x1; global x2;
    x_min, x_max = min(x1) - .5, max(x1) + .5
    y_min, y_max = min(x2) - .5, max(x2) + .5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.055), np.arange(y_min, y_max, 0.055))
    Z = np.empty((0,), dtype=int)
    #print( np.shape(xx) )
    #print( np.shape(yy) )
    for i in range(len(xx)):
        for j in range(len(yy[1])):
            Z = np.append(Z,[ g( np.array( [[xx[i][j]], [yy[i][j]]] ) ) ])
    Z = Z.reshape(xx.shape)

    plt.pcolormesh(xx, yy, Z, cmap=plt.cm.Paired)

    # Plot also the training points
    plt.xlabel('x1')
    plt.ylabel('x2')

    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.xticks(())
    plt.yticks(())

    plt.show()

def q2(filename):
    ctr  = 0
    tctr = 0
    with open(filename, "r") as f2:
        f2.readline()
        for line in f2:
            ops = list(map(float, line.split(sep=',')))
            p = np.array([ [ops[0]], [ops[1]] ])
            if g(p) == int(ops[2]):
                ctr += 1
            tctr += 1

    return float(ctr)/tctr


with open("datatrain.csv", "r") as f:
    f.readline()
    for line in f:
        ops = list(map(float, line.split(sep=',')))
        if int(ops[2]) == 2:
            meanc2x1[0] += ops[0]
            meanc2x1[1] += 1
            meanc2x2[0] += ops[1]
            meanc2x2[1] += 1
            whichClass(ops[0], 1, 2)
            whichClass(ops[1], 2, 2)
        elif int(ops[2]) == 1:
            meanc1x1[0] += ops[0]
            meanc1x1[1] += 1
            meanc1x2[0] += ops[1]
            meanc1x2[1] += 1
            whichClass(ops[0], 1, 1)
            whichClass(ops[1], 2, 1)
        elif int(ops[2]) == 0:
            meanc0x1[0] += ops[0]
            meanc0x1[1] += 1
            meanc0x2[0] += ops[1]
            meanc0x2[1] += 1
            whichClass(ops[0], 1, 0)
            whichClass(ops[1], 2, 0)
        else:
            raise "Error"
        x1.append(ops[0])
        x2.append(ops[1])
        cs.append(int(ops[2]))

    meanc0x1[2] = meanc0x1[0] / meanc0x1[1]
    meanc0x2[2] = meanc0x2[0] / meanc0x2[1]
    meanc1x1[2] = meanc1x1[0] / meanc1x1[1]
    meanc1x2[2] = meanc1x2[0] / meanc1x2[1]
    meanc2x1[2] = meanc2x1[0] / meanc2x1[1]
    meanc2x2[2] = meanc2x2[0] / meanc2x2[1]

x = np.array( [[1], [2]] )
myGraph()
print( "Accuracy is: " + str(q2("datatest.csv") *100 ) + "%.")
