'''
    Three ways to harvest and to fit the trajectory from the user interface
'''

import matplotlib.pyplot as plt
from scipy import signal
import xlrd
import numpy as np

# Give the location of the file
loc = ("Trajectories_storing6.xls")

#Give the scale of the draw
scale = 1000

# columns in the excel file
columnX = 8
columnY = 9

def importTrajectory0():
    '''
        no modification
    '''
    X = []
    Y = []

    # To open Workbook
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)

    j= 0
    increment = 5   #minimal distance between two points

    # While there is something to read in the excel file
    while isinstance(sheet.cell_value(j, columnX),float) :
        X.append(sheet.cell_value(j, columnX)*scale)
        Y.append(sheet.cell_value(j, columnY)*scale)
        j+=1
    plt.plot(X,Y,label='original')
    return [X,Y]

def importTrajectory1():
    '''
        Spatial sampling
    '''
    X = []
    Y = []

    # To open Workbook
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)

    j= 0
    i = 0
    increment = 15   #minimal distance between two points

    # While there is something to read in the excel file
    while isinstance(sheet.cell_value(j, columnX),float) :
        if j != 0 :
            if np.linalg.norm(np.subtract([X[i-1],Y[i-1]],[sheet.cell_value(j, columnX)*scale,sheet.cell_value(j, columnY)*scale])) > increment:
                X.append(sheet.cell_value(j, columnX)*scale)
                Y.append(sheet.cell_value(j, columnY)*scale)
                i+=1
        else :
            X.append(sheet.cell_value(j, columnX)*scale)
            Y.append(sheet.cell_value(j, columnY)*scale)
            i+=1

        j+=1
    plt.plot(X,Y,label='spatial sampling')
    return [X,Y]

def importTrajectory2():
    '''
        Temporal sampling
    '''
    X = []
    Y = []

    # To open Workbook
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)

    j= 0
    counter = 0
    increment = 10  # One point out of increment is taken
    while isinstance(sheet.cell_value(counter*increment, columnX),float) :
        if j == 0 :
            X.append(sheet.cell_value(counter*increment, columnX)*scale)
            Y.append(sheet.cell_value(counter*increment, columnY)*scale)
            j = 0
            counter +=1
        else :
            j+=1
    plt.plot(X,Y,label='temporal sampling')
    return [X,Y]

def importTrajectory3():
    '''
        filtering : the trajectory is smoothen
    '''
    X = []
    Y = []

    # To open Workbook
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)

    i = 0
    while isinstance(sheet.cell_value(i, 6),float) :
        X.append(sheet.cell_value(i, 6)*scale)
        Y.append(sheet.cell_value(i, 7)*scale)
        i += 1
    # X and Y are filter :
    # savgol_filter(signal,sizeWindow,Order of the polynom)
    X=signal.savgol_filter(X, 55, 8)
    Y=signal.savgol_filter(Y, 55, 8)
    plt.plot(X,Y,label='filtering')
    return [X,Y]

if __name__ == "__main__":
    [X0,Y0] = importTrajectory0()
    [X1,Y1] = importTrajectory1()
    [X2,Y2] = importTrajectory2()
    [X3,Y3] = importTrajectory3()   #not satisfying
    plt.axis('equal')
    plt.legend()
    plt.show()
