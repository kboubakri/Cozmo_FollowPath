'''
    Useful mathematical functions
'''

from math import sqrt,cos,sin,acos,pi,atan2
import numpy as np


def correctionAngle(angle):
    '''
        Return the smallest ORIENTED angle between two angle
    '''
    r = abs(angle)%360
    if r > 180:
        r = 360-r
    if (angle>0 and angle<=180)or(angle<=-180 and angle>=-360):
        return r
    else :
        return -r

def is_between(begin,point,end):
    '''
        Return True if the point is on the segment (begin,end)
        Only consider the x coordinate (return True if the point is above the segment)
        Is sufficient for our algorithm
    '''
    if point[0]>=min(begin[0],end[0]) and point[0]<=max(begin[0],end[0]):
        return True
    else :
        return False

def angleBetweenVectors(u,v):
    '''
        Return the ORIENTED angle between two vectors
        using the orthogonal projection
        cf the wikipedia page of the orthogonal projection
    '''
    term1 = u[0]*v[1] - v[0]*u[1]
    term2 = u[0]*v[0] + v[1]*u[1]
    return(atan2(term1,term2))

def distanceBetweenPoint(xp,yp,xt,yt):
    '''
        Return the euclidean distance between two points
    '''
    dx = xt-xp
    dy = yp-yt
    return sqrt(dx**2+dy**2)

def unitVector(v):
    '''
        Return the normalized vector (norm(v_normalized)==1)
    '''
    return(v/np.linalg.norm(v))

def euclideanVector(begin,end):
    '''
        Return the euclidean vector of a segment
    '''
    return([end[0]-begin[0],end[1]-begin[1]])

if __name__ == "__main__":
    u = [0,0]
    v = [10,10]
    correctedAngle = correctionAngle(351)
    bool = is_between(u,[5,5],v)
    angle = angleBetweenVectors(u,v)
    d = distanceBetweenPoint(1,1,0,0)
    unitV = unitVector(v)
    dir = euclideanVector(u,v)
