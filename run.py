import display as disp
import algebra as alg
import trajectoryManager as traj
import conversionSpeed as speed
import prediction as predic
import pathFollowingAlgorithm as follow
from cozmo.util import degrees, Pose,Position,distance_mm, speed_mmps,radians
import cozmo
import time

def pointsToPath(X,Y):
    '''
        Return the coordinate of all the point of the trajectory as a unique list
    '''
    p = []
    for i in range(0,len(X)-1,1):
        p.append([X[i],Y[i]])
    return p

def initialState(p,robot: cozmo.robot.Robot):
    '''
        The robot drive to the first position with the right orientation
    '''
    [vr,vl] = [25,24]
    angle = robot.pose.rotation.angle_z.radians
    orientation = predic.orientationTarget(p[0],p[1])
    firstAngle = alg.angleBetweenVectors([10,0],orientation)    #Robot heading towoard the next posiition
    #The robot drive to the first position
    robot.go_to_pose(Pose(p[0][0],p[0][1],0,angle_z=radians(firstAngle))).wait_for_completed()
    return[vr,vl,firstAngle]

def cozmo_program(robot: cozmo.robot.Robot):
    '''
        Main
    '''
    [X,Y] = traj.importTrajectory2()
    p = pointsToPath(X,Y)
    [vr,vl,angle] = initialState(p,robot)
    begin = time.time()
    follow.followComposedTrajectory(robot,p,p[0],vl,vr,angle)
    print("execution time :",time.time()-begin)

cozmo.run_program(cozmo_program)
