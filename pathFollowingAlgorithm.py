'''
    The algorithm per se. find the subpath to follow and compute the new wheel speeds
'''

import display as disp
import algebra as alg
from trajectoryManager import scale
import conversionSpeed as speed
import prediction as predic
import cozmo
import matplotlib.pyplot as plt
from math import pi
import time
import numpy as np

radius = 1  #Acceptable distance from the path in mm
deltaT = 0.4    #time between two instructions in s
deltaD =5  #Look ahead distance in mm
maxSpeed = 25   #mm/s
error = 0   #mean squarred error in mm

def newWheelsSpeed(vr,vl,position,begin,end,angle,pathPositions):
    '''
        Return the next speed instructions
        computed from the actual state of the robot and the path
    '''
    global error
    [v,omega] = speed.speedWheelsToLinearSpeed(vr,vl)
    linearSpeed = speed.linearSpeedToAxisSpeed(v,omega,angle)
    nextPos = predic.predictionNextPosition(linearSpeed,position)
    n = predic.neareastPoint(begin,end,nextPos)
    error += alg.distanceBetweenPoint(position[0],position[1],n[0],n[1])
    if np.all(n == nextPos) == True :   #If the next position is close enough to the path
        disp.displayAll(pathPositions,position,nextPos,nextPos,0,0,n)
        return [vr,vl,nextPos[0],nextPos[1],angle]
    else :  #Correction the speed instruction
        targetPos = predic.positionTarget(n,alg.euclideanVector(begin,end))
        orientation = predic.orientationTarget(position,targetPos)
        newSpeed = np.dot(orientation,maxSpeed)
        disp.displayAll(pathPositions,position,nextPos,nextPos,0,0,targetPos)
        #the angular speed must reflect the current orientation and how it must be corrrected
        newAngle = alg.angleBetweenVectors([10,0],newSpeed)
        omega = 2*alg.correctionAngle((newAngle-angle)*180/pi)*pi/180*deltaT
        newWheelsSpeed = speed.linearSpeedToWheels(np.linalg.norm(newSpeed),omega)
        return [newWheelsSpeed[0],newWheelsSpeed[1],nextPos[0],nextPos[1],newAngle]

def followComposedTrajectory(robot:cozmo.robot.Robot,pathPositions,pPosition,vl,vr,angle):
    '''
        Path Following Algorithm
    '''
    stateVector = [vr,vl,pPosition[0],pPosition[1],angle]
    subPath = 0
    nbSubPath = len(pathPositions)-1
    i = 0
    #While the robot is not close enough of the last position of the trajectory
    while np.linalg.norm(alg.euclideanVector([robot.pose.position.x,robot.pose.position.y],pathPositions[nbSubPath])) > scale/10 :
        #The robot drive with the instructions computed with newWheelsSpeed
        robot.drive_wheels(stateVector[1],stateVector[0])
        time.sleep(deltaT)  #During a certain time
        plt.scatter([robot.pose.position.x],[robot.pose.position.y])    #Plot the real position of the robot
        stateVector = newWheelsSpeed(stateVector[0],stateVector[1],[robot.pose.position.x,robot.pose.position.y],pathPositions[subPath],pathPositions[subPath+1],robot.pose.rotation.angle_z.radians,pathPositions)
        subPath = predic.closestPath(subPath,pathPositions,[robot.pose.position.x,robot.pose.position.y])
        i+=1
    print("Mean error : ",error/i)
