"""
Created by Safa Keskin, March 4, 2018
BLG454E - Learning From Data - Assignment 1
"""

import sys
import math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab

#function that reads data
def readData( path ):
	data = []
	file = open(path, 'r')
	for line in file:
		data += [float(line)]	
	file.close()
	return data

#function that calculates mean
def calculateMean( data ):
	sum = 0
	for i in data:
		sum += i
	return sum / len(data)

#function that operates maximum likelihood estimation
def mle( data ):
	mean = calculateMean( data )
	sum  = 0
	#calculating variance
	for i in data:
		sum += math.pow((i - mean), 2)
	return  mean, sum / len( data )


data = readData( sys.argv[1] )
#print( data )
mean, variance = mle(data)
sigma		   = math.sqrt(variance)

#-- Line PART
x = np.linspace( mean - 3*sigma, mean + 3*sigma, 100 )

# Histogram PART
myhist = plt.hist(data, 25, normed=1, facecolor='g', alpha=0.75)
plt.title('Maximum Likelihood Estimation')
plt.text(4, .14, r'$\mu=10,\ \sigma=2.57$')
plt.axis([0, max(data), 0, 0.17])
plt.grid(False)

#plotting part
plt.plot(x, mlab.normpdf( x, mean, sigma ))
print(mean, sigma)

plt.show()
