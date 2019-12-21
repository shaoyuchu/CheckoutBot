import socket
import sys
import numpy as np
import cv2
import time
from image import take_pictures, mapping
from connect import connect2Arm

if __name__ == "__main__":

    # [[x, y], [x, y], [x, y]]
    actual_pos = np.array([[-100.0, 380.0], [200.0, 550.0], [100.0, 400.0]])
    img_pos = np.zeros([3, 2])
    s = connect2Arm()

    for i in range(3):

        # move to position
        action = 'MOVP ' + str(actual_pos[i, 0]) + ' ' + str(actual_pos[i, 1]) + ' -170 90 0 180'
        s.sendall(action.encode('ascii'))

        # place the item
        input('Please place the object in the gripper.')

        # home
        goHome = 'GOHOME'
        s.sendall(goHome.encode('ascii'))
        time.sleep(5)

        # get centroid, store in img_pos
        mc, p_angle = take_pictures()
        img_pos[i, 0] = mc[0][0]
        img_pos[i, 1] = mc[0][1]
        print('mc for calibration: ', img_pos[i, 0], ', ', img_pos[i, 1])
        input('Please remove the object.')
    
    s.close()

    # compute and store the mapping matrix
    print("actual: ", actual_pos)
    print("img: ", img_pos)
    img2actual = mapping(actual_pos, img_pos)
    np.save('img2actual.npy', img2actual)
    print(np.matmul(img2actual, img_pos))
    print('\'img2actual.npy\' saved')
