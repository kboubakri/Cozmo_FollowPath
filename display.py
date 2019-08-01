'''
    Functions used to display important variables
'''

import numpy as np
import matplotlib.pyplot as plt

#incremental variable for the image saving
i = 0

def connectpoints(x,y):
    '''
        Draw a lign between a series of points
    '''
    for i in range(0, len(x), 1):
        plt.plot(x[i:i+2], y[i:i+2], 'k-')

def connectNearestPoint(x,y,xn,yn):
    '''
        Draw a lign between a point and its neareast point on a segment
    '''
    plt.plot([x,xn],[y,yn],'g')

#def displayVectors(V,pPosition):
#    '''
#        Display a series of vectors V departing from a certain position
#    '''
#    origin = [pPosition[0]], [pPosition[1]] # origin point
#    plt.quiver(*origin, V[:,0], V[:,1], color=['r','b','g'], scale=1)

def displayVector(V,pPosition):
    '''
        Display a vector V departing from a certain position
    '''
    origin = [pPosition[0]], [pPosition[1]] # origin point
    plt.quiver(*origin, V[0], V[1], color=['r','b','g'], scale=1)

def getColumn(matrix, i):
    '''
        Return the i-column of a matrix
    '''
    return [row[i] for row in matrix]

def displayAll(pathPositions,pPosition,pPredict,pTarget,oldSpeed,newSpeed,neareastPoint):
    '''
        Display all the important parameters for the path following algorithm
    '''
    global i
    plt.title('robot following a trajectory')
    plt.xlabel('x axis in mm')
    plt.ylabel('y axis in mm')
    #Get the coordinate of each pooint of the trajectory
    x = getColumn(pathPositions,0)
    y = getColumn(pathPositions,1)
    #Get the old and the new vector speed
    V = [oldSpeed,newSpeed]
    displayVector(V,pPosition)
    connectpoints(x,y)
    connectNearestPoint(pPosition[0],pPosition[1],neareastPoint[0],neareastPoint[1])
    plt.plot(x, y, 'ro')
    plt.axis('equal')
    plt.draw()
    # Save the current image and give it the number i
    #plt.savefig('CorrespondingVideo{0}.png'.format(i))
    i+=1    #increment the image number
    plt.pause(0.1)
    plt.clf()

def displayShortestDistance(pathPositions,point,n):
    '''
        Display the shortest distance between the point and the path positions
    '''
    x,y = zip(*pathPositions)
    plt.plot(x,y)
    plt.plot([point[0],n[0]],[point[1],n[1]],'k-')
    plt.show()
    plt.pause(0.1)
    plt.close()
