import socket
import sys
import numpy as np
import cv2
import math
from image import take_pictures, mapping
from connect import connect2Arm
from detect import *

# json implementation, fast
# import json
# f =  open('./obj_data/obj_info.json')
# data = json.load(f)
# f.close()

# csv implementation, clear
# import pandas as pd
# df = pd.read_csv('./obj_data/obj_info.csv', index_col=0)
# print(df['weight'][1]) # 20


A = np.load('./calibration_data/img2actual.npy')
pixel2mm = np.load('./calibration_data/pixel2mm.npy')
number_of_objects = 1
step_by_step = True


def checkPoint(val):
    if step_by_step:
        print(val)
        input()


if __name__ == "__main__":
    
    mc, p_angle = take_pictures()
    s = connect2Arm()
    
    for i in range(0, number_of_objects):
        
        # compute the actual position
        img_p = [[mc[i][0]], [mc[i][1]], [1]]
        p_hat = np.matmul(A, img_p)
        p_hat = np.reshape(p_hat, 3)

        # move above the target
        val = 'MOVP ' + str(p_hat[0]) + ' ' + str(p_hat[1]) + ' 0 ' + str(-p_angle[i]) + ' 0 180\n'
        checkPoint(val)
        s.sendall(val.encode('ascii'))
        

        # move down to reach the target
        val = 'MOVP ' + str(p_hat[0]) + ' ' + str(p_hat[1]) + ' -185 ' + str(-p_angle[i]) + ' 0 180\n'
        checkPoint(val)
        s.sendall(val.encode('ascii'))
        

        # close the gripper
        s.sendall(close_grip.encode('ascii'))
        

        detect(i, s)

    # go home
    go_home = 'GOHOME\n'
    s.sendall(go_home.encode('ascii'))
    
    print(data)

    s.close()
