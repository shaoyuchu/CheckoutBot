import socket
import sys
import numpy as np
import cv2
import math
from image import take_pictures, mapping
from connect import connect2Arm
from detect import *

A = np.load('img2actual.npy')
number_of_objects = 3
step_by_step = False


def checkPoint(val):
    if step_by_step:
        print(val)
        input()


if __name__ == "__main__":
    
    mc, p_angle = take_pictures()
    s = connect2Arm()
    
    for i in range(1, number_of_objects):

        # compute the actual position
        img_p = [[mc[i][0]], [mc[i][1]], [1]]
        p_hat = np.matmul(A, img_p)
        p_hat = np.reshape(p_hat, 3)

        # move above the target
        val = 'MOVP ' + str(p_hat[0]) + ' ' + str(p_hat[1]) + ' 0 ' + str(-p_angle[i]) + ' 0 180'
        checkPoint(val)
        s.sendall(val.encode('ascii'))
        data = s.recv(1024)

        # move down to reach the target
        val = 'MOVP ' + str(p_hat[0]) + ' ' + str(p_hat[1]) + ' -200 ' + str(-p_angle[i]) + ' 0 180'
        checkPoint(val)
        s.sendall(val.encode('ascii'))
        data = s.recv(1024)

        # close the gripper
        s.sendall(close_grip.encode('ascii'))
        data = s.recv(1024)

        # detect(i, s)

        # lift the target vertically
        val = 'MOVP ' + str(p_hat[0]) + ' ' + str(p_hat[1]) + ' 0 ' + str(-p_angle[i]) + ' 0 180'
        checkPoint(val)
        s.sendall(val.encode('ascii'))
        data = s.recv(1024)
        
        # compute the actual position of the destination
        img_p = [[mc[0][0]], [mc[0][1]], [1]]
        p_hat = np.matmul(A, img_p)
        p_hat = np.reshape(p_hat, 3)

        # pile up
        if i == 2:
            val = 'MOVP ' + str(p_hat[0]) + ' ' + str(p_hat[1]) + ' -120 ' + str(-p_angle[0]) + ' 0 180'
        else:
            val = 'MOVP ' + str(p_hat[0]) + ' ' + str(p_hat[1]) + ' -155 ' + str(-p_angle[0]) + ' 0 180'
        checkPoint(val)
        s.sendall(val.encode('ascii'))
        data = s.recv(1024)

        # open the gripper, release the target
        checkPoint('Grip')
        s.sendall(open_grip.encode('ascii'))
        data = s.recv(1024)

        # move upward vertically
        val = 'MOVP ' + str(p_hat[0]) + ' ' + str(p_hat[1]) + ' 0 ' + str(-p_angle[0]) + ' 0 180'
        checkPoint(val)
        s.sendall(val.encode('ascii'))
        data = s.recv(1024)

    # go home
    go_home = 'GOHOME'
    checkPoint(go_home)
    s.sendall(go_home.encode('ascii'))
    data = s.recv(1024)
    print(data)

    s.close()
