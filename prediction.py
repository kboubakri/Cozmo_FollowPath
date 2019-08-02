'''
    All the functions linked to the prediction behaviour of the robot
'''


import algebra as alg
from math import sqrt,cos,sin,acos,pi,atan2
import numpy as np

deltaT = 0.4    #s


def predictionNextPosition(linearSpeed,position):
    '''
        Return the predicted next position of the robot
        Considering its current position and speed
    '''
    distance = np.dot(linearSpeed,deltaT)
    return np.add(position,distance)

def neareastPoint(begin,end,point):
    '''
        Return the neareast point of the robot on a certain subPath (segment)
        using the orthogonal projection
    '''
    from pathFollowingAlgorithm import radius
    v = np.subtract(end,begin)
    normV = np.linalg.norm(v)
    #Compute the nearest point coordinate thanks to orthogonal projection
    distance = ((point[0]-begin[0])*v[0] + (point[1]-begin[1])*v[1])/normV
    xn = begin[0] + (distance/normV)*v[0]
    yn = begin[1] + (distance/normV)*v[1]
    distanceToPath = np.linalg.norm(np.subtract(point,[xn,yn]))
    #if the robot is too far from the path
    if abs(distanceToPath) > radius :
        return[xn,yn]   # return its nearest point coordinate
    else :
        return point    #return its coordinate

def smallestDistance(begin,end,point):
    '''
        Return the smallest distance between the robot and the subpath
        as well as the coordinate of the nearest point
    '''
    v = alg.euclideanVector(begin,end)
    normV = np.linalg.norm(v)
    #Compute the nearest point coordinate thanks to orthogonal projection
    distance = ((point[0]-begin[0])*v[0] + (point[1]-begin[1])*v[1])/normV
    xn = begin[0] + (distance/normV)*v[0]
    yn = begin[1] + (distance/normV)*v[1]
    n = [xn,yn]
    dx = xn - point[0]
    dy = yn - point[1]
    return [sqrt(dx**2+dy**2),n]

'''Compute the position of the target using the neareast point on a subtrajectory
 and its euclidean vector'''
def positionTarget(neareastPoint,euclideanvector):
    from pathFollowingAlgorithm import deltaD
    euclideanvector = alg.unitVector(euclideanvector)
    vDistance = np.dot(euclideanvector,deltaD)
    return np.add(neareastPoint,vDistance)

'''Return the vector between the robot and its target'''
def orientationTarget(pRobot,pTarget):
    return alg.unitVector(alg.euclideanVector(pRobot,pTarget))

'''Return the closest subPath from the robot'''
def closestPath(lastSubPath,pathPositions,point):
    [number,closest] = [-1,1000]    #path number, distance to robot
    #Every path after the one currently considered and except the last one
    if lastSubPath < len(pathPositions)-1:
        for i in range(lastSubPath,(len(pathPositions)-1)):
            [d,n] = smallestDistance(pathPositions[i],pathPositions[i+1],point)
            t = positionTarget(n,alg.euclideanVector(pathPositions[i],pathPositions[i+1]))
            #The robot should follow a close path as much as possible
            begin = pathPositions[lastSubPath]
            end = pathPositions[lastSubPath+1]
            if i == lastSubPath and alg.is_close_to_path(n,end,begin):
                if  d < closest+1 :
                    closest = d
                    number = i
            else :
                #If the closest paths are not ideal, let's consider the other paths
                if  d < closest+1 and alg.is_between(pathPositions[i],n,pathPositions[i+1]):
                    closest = d
                    number = i
        if number != -1 and closest != 1000:    #if the robot found a patht to follw
            [d,n] = smallestDistance(pathPositions[number],pathPositions[number+1],point)
            print("subPath :",number,"  distance :",alg.is_close_to_path(n,end,begin),    "is on the path ?",alg.is_between(pathPositions[number],n,pathPositions[number+1]))
            return number
        else :  # we move to the next path
            return lastSubPath+1
    else :  #we stay on the last path
        return lastSubPath


if __name__ == "__main__":
    begin = [0,0]
    end = [10,10]
    p = [5,5]
    linearSpeed = 50
    p = predictionNextPosition(linearSpeed,p)
    n = neareastPoint(begin,end,p)
    d = smallestDistance(begin,end,p)
    t = positionTarget(n,np.subtract(end,begin))
    o = orientationTarget(p,t)
