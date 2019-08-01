'''
    Functions needed to switch from linear, axis and wheel speeds
'''

from math import sqrt,cos,sin,acos,pi,atan2
import numpy as np

baseWheels = 45 # distance between the wheels in mm
lx = 5  #mm #Distance between the center of the robot and a virtual point

def linearSpeedToWheels(v,omega):
    '''
        Return the speed of each wheel computed from the linear and angular speed
    '''
    transform = np.array([[1,baseWheels/2],[1,-baseWheels/2]])
    state = np.array([v,omega])
    state = state.transpose()
    result = transform.dot(state)
    return result

def speedWheelsToLinearSpeed(vr,vl):
    '''
        Return the linear and angular speed computed from the speed of each wheel
    '''
    transform = np.array([[-baseWheels/2,-baseWheels/2],[-1,1]])
    transform = transform/(-baseWheels)
    state = np.array([vr,vl])
    state = state.transpose()
    result = transform.dot(state)
    return result

def linearSpeedToAxisSpeed(v,omega,theta):
    '''
        Return the speed on each axis computed from the linear and angular speed
        as well as the current angle
    '''
    vx = v*cos(theta)-lx*omega*sin(theta)
    vy = v*sin(theta)+lx*omega*cos(theta)
    return[vx,vy]

if __name__ == "__main__":
    [v,omega] = [10,10]
    [vr,vl] = linearSpeedToWheels(v,omega)
    [vx,vy] = linearSpeedToAxisSpeed(v,omega,0)
    [v,omega] = speedWheelsToLinearSpeed(vr,vl)
