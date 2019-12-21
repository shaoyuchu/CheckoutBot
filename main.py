

import socket
import sys


import socket
import numpy as np
import cv2
import math
from image import take_pictures, mapping
# from connect import connect2Arm

# [[x],[y],[1]]

# mapping
actual = [[-132.0847, 236.6651, 91.935104], [390.27371,411.77688, 574.30101], [1,1,1]]
img = [[469.51339957488125, 77.10519952646561,230.15167559590046], [131.64767848311172, 142.55809317365495, 315.3116258908931], [1,1,1]]
A = mapping(actual, img)

number_of_objects = 3

if __name__ == "__main__":
    mc, p_angle = take_pictures()
    # s = connect2Arm()
    # ## Move to above object 1
    # for i in range(1, number_of_objects):

    #     img_p = [[mc[i][0]], [mc[i][1]], [1]]
    #     p_hat = np.matmul(A, img_p)
    #     p_hat = np.reshape(p_hat, 3)
    #     print(img_p, p_hat)
    #     val = "MOVP " + str(p_hat[0,0]) +" "+ str(p_hat[0,1]) + " 0 " + str(-p_angle[i]) +" 0 180"
    #     print(val)
    #     input()
    #     s.sendall(val.encode('ascii'))

    #     val = "MOVP " + str(p_hat[0,0]) +" "+ str(p_hat[0,1]) + " -200 " + str(-p_angle[i]) +" 0 180"
    #     print(val)
    #     input()
    #     s.sendall(val.encode('ascii'))

    #     val = "OUTPUT 48 ON"
    #     s.sendall(val.encode('ascii'))


    #     val = "MOVP " + str(p_hat[0,0]) +" "+ str(p_hat[0,1]) + " 0 " + str(-p_angle[i]) +" 0 180"
    #     print(val)
    #     input()
    #     s.sendall(val.encode('ascii'))

    #     ## Finish grabing Object 1
    #     img = np.matrix(img)
    #     A = np.matmul( actual, img.I)
    #     # print(A)
    #     img_p = [[mc[0][0]], [mc[0][1]], [1]]
    #     p_hat = np.matmul(A, img_p)
    #     p_hat = np.reshape(p_hat, 3)
    #     print(p_hat)

    #     if i == 2:
    #         val = "MOVP " + str(p_hat[0,0]) +" "+ str(p_hat[0,1]) + " -122 " + str(-p_angle[0]) +" 0 180"
    #     else:
    #         val = "MOVP " + str(p_hat[0,0]) +" "+ str(p_hat[0,1]) + " -160 " + str(-p_angle[0]) +" 0 180"
    #     print(val)
    #     input()
    #     s.sendall(val.encode('ascii'))

    #     val = "OUTPUT 48 OFF"
    #     input()
    #     s.sendall(val.encode('ascii'))


    #     val = "MOVP " + str(p_hat[0,0]) +" "+ str(p_hat[0,1]) + " 0 " + str(-p_angle[0]) +" 0 180"
    #     print(val)
    #     input()
    #     s.sendall(val.encode('ascii'))

    # input()
    # goHome = "GOHOME"
    # s.sendall(goHome.encode('ascii'))
    # data = s.recv(1024)
    # print(data)

    # s.close()
