import socket
import sys
import numpy as np
import cv2
from image import take_pictures, mapping
from connect import connect2Arm

if __name__ == "__main__":

    actual_pos = np.array([[-100, 200, 100], [390, 420, 550], [1, 1, 1]])
    img_pos = np.array([[0, 0, 0], [0, 0, 0], [1, 1, 1]])
    s = connect2Arm()

    for i in range(3):

        # move to position
        action = 'MOVP ' + str(actual_pos[i, 0]) + ' ' + str(actual_pos[i,1]) + ' 0 90 0 180'
        s.sendall(action.encode('ascii'))

        # place the item
        input('Please place the object in the gripper.')

        # home
        goHome = 'GOHOME'
        s.sendall(goHome.encode('ascii'))

        # get centroid, store in img_pos
        mc, p_angle = take_pictures()
        img_pos[i, 0] = [mc[0][0]]
        img_pos[i, 1] = [mc[0][1]]
        print('mc for calibration: ', img_pos[i, 0], ', ', img_pos[i, 1])
    
    s.close()

    # compute and store the mapping matrix
    img2actual = mapping(actual_pos, img_pos)
    np.save('img2actual.npy', img2actual)
    print('\'img2actual.npy\' saved!')
