import socket
import sys
import numpy as np
import cv2
import math
from image import take_pictures, mapping
from connect import connect2Arm

# [[x],[y],[1]]
# mapping
# actual = [[-132.0847, 236.6651, 91.935104], [390.27371,411.77688, 574.30101], [1,1,1]]
# img = [[469.51339957488125, 77.10519952646561,230.15167559590046], [131.64767848311172, 142.55809317365495, 315.3116258908931], [1,1,1]]
# A = mapping(actual, img)
A = np.load('img2actual.npy')
print('A', A)
number_of_objects = 3
step_by_step = False

if __name__ == "__main__":
    
    mc, p_angle = take_pictures()
    s = connect2Arm()
    
    for i in range(1, number_of_objects):

        img_p = [[mc[i][0]], [mc[i][1]], [1]]
        p_hat = np.matmul(A, img_p)
        p_hat = np.reshape(p_hat, 3)
        print(img_p, p_hat)
        val = "MOVP " + str(p_hat[0]) +" "+ str(p_hat[1]) + " 0 " + str(-p_angle[i]) +" 0 180"
        if step_by_step:
            print(val)
            input()
        s.sendall(val.encode('ascii'))

        val = "MOVP " + str(p_hat[0]) +" "+ str(p_hat[1]) + " -200 " + str(-p_angle[i]) +" 0 180"
        if step_by_step:
            print(val)
            input()
        s.sendall(val.encode('ascii'))

        val = "OUTPUT 48 ON"
        s.sendall(val.encode('ascii'))


        val = "MOVP " + str(p_hat[0]) +" "+ str(p_hat[1]) + " 0 " + str(-p_angle[i]) +" 0 180"
        if step_by_step:
            print(val)
            input()
        s.sendall(val.encode('ascii'))

        img_p = [[mc[0][0]], [mc[0][1]], [1]]
        p_hat = np.matmul(A, img_p)
        p_hat = np.reshape(p_hat, 3)
        print(p_hat)

        if i == 2:
            val = "MOVP " + str(p_hat[0]) +" "+ str(p_hat[1]) + " -120 " + str(-p_angle[0]) +" 0 180"
        else:
            val = "MOVP " + str(p_hat[0]) +" "+ str(p_hat[1]) + " -155 " + str(-p_angle[0]) +" 0 180"
        if step_by_step:
            print(val)
            input()
        s.sendall(val.encode('ascii'))

        val = "OUTPUT 48 OFF"
        if step_by_step:
            input()
        s.sendall(val.encode('ascii'))


        val = "MOVP " + str(p_hat[0]) +" "+ str(p_hat[1]) + " 0 " + str(-p_angle[0]) +" 0 180"
        if step_by_step:
            print(val)
            input()
        s.sendall(val.encode('ascii'))

    if step_by_step:
        input()
    goHome = "GOHOME"
    s.sendall(goHome.encode('ascii'))
    data = s.recv(1024)
    print(data)

    s.close()
